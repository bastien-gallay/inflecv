import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from scripts.lib import ValidatedContent

REQUIRED_SECTIONS = [
    "Expérience",
    "Formation",
    "Certifications",
]

EMAIL_PATTERN = re.compile(r"email:\s*[\"']?[\w.+-]+@[\w.-]+\.\w+[\"']?", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"phone:", re.IGNORECASE)
LINKEDIN_PATTERN = re.compile(r"linkedin:", re.IGNORECASE)
# Match both "#entry(" and "= entry(" (variable assignment)
ENTRY_PATTERN = re.compile(r"(?:#entry\(|=\s*entry\()")
TRAILING_WHITESPACE_PATTERN = re.compile(r"[ \t]+$", re.MULTILINE)
ENCODING_ERROR_PATTERN = re.compile(r"\?{3,}")
FRENCH_CHARS_PATTERN = re.compile(r"[éèêëàâäùûüîïôöç]", re.IGNORECASE)


@dataclass
class FormatResult:
    success: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    sections_found: list[str] = field(default_factory=list)
    entry_count: int = 0
    line_count: int = 0
    char_count: int = 0


FormatStep = Callable[["FormatContext"], "FormatContext"]


@dataclass
class FormatContext:
    content: ValidatedContent
    result: FormatResult

    def bind(self, func: FormatStep) -> "FormatContext":
        if not self.result.success:
            return self
        return func(self)

    def map(self, func: FormatStep) -> "FormatContext":
        return func(self)


def check_sections(content: str) -> tuple[list[str], list[str]]:
    found = []
    missing = []
    for section in REQUIRED_SECTIONS:
        if section in content:
            found.append(section)
        else:
            missing.append(section)
    return found, missing


def check_contact_info(content: str) -> tuple[list[str], list[str]]:
    found = []
    missing = []

    if EMAIL_PATTERN.search(content):
        found.append("email")
    else:
        missing.append("email")

    if PHONE_PATTERN.search(content):
        found.append("phone")
    else:
        missing.append("phone")

    if LINKEDIN_PATTERN.search(content):
        found.append("linkedin")
    else:
        missing.append("linkedin")

    return found, missing


def count_entries(content: str) -> int:
    return len(ENTRY_PATTERN.findall(content))


def check_trailing_whitespace(content: str) -> int:
    return len(TRAILING_WHITESPACE_PATTERN.findall(content))


def check_encoding_errors(content: str) -> bool:
    return bool(ENCODING_ERROR_PATTERN.search(content))


def check_french_chars(content: str) -> bool:
    return bool(FRENCH_CHARS_PATTERN.search(content))


def step_fill_statistics(ctx: FormatContext) -> FormatContext:
    ctx.result.line_count = len(ctx.content.split("\n"))
    ctx.result.char_count = len(ctx.content)
    return ctx


def step_verify_sections(ctx: FormatContext) -> FormatContext:
    found, missing = check_sections(ctx.content)
    ctx.result.sections_found = found
    for section in missing:
        ctx.result.warnings.append(f"Section '{section}' manquante")
    return ctx


def step_verify_contact(ctx: FormatContext) -> FormatContext:
    _, missing = check_contact_info(ctx.content)
    for item in missing:
        if item == "email":
            ctx.result.errors.append("Email manquant ou invalide")
            ctx.result.success = False
        else:
            ctx.result.warnings.append(f"{item.capitalize()} manquant")
    return ctx


def step_verify_entries(ctx: FormatContext) -> FormatContext:
    ctx.result.entry_count = count_entries(ctx.content)
    if ctx.result.entry_count < 5:
        ctx.result.warnings.append(f"Peu d'entrées dans le CV ({ctx.result.entry_count})")
    return ctx


def step_verify_whitespace(ctx: FormatContext) -> FormatContext:
    trailing_ws = check_trailing_whitespace(ctx.content)
    if trailing_ws > 0:
        ctx.result.warnings.append(f"{trailing_ws} lignes avec espaces en fin de ligne")
    return ctx


def step_verify_encoding(ctx: FormatContext) -> FormatContext:
    if check_encoding_errors(ctx.content):
        ctx.result.errors.append("Caractères d'encodage invalides (???) détectés")
        ctx.result.success = False
    return ctx


def step_verify_french_chars(ctx: FormatContext) -> FormatContext:
    if not check_french_chars(ctx.content):
        ctx.result.warnings.append("Pas de caractères accentués détectés")
    return ctx


def collect_typ_content(src_dir: Path) -> str:
    """Collect content from all .typ files in src directory."""
    contents = []
    for typ_file in sorted(src_dir.rglob("*.typ")):
        contents.append(typ_file.read_text(encoding="utf-8"))
    return "\n".join(contents)


def verify_format(project_root: Path | None = None) -> FormatResult:
    if project_root is None:
        project_root = Path.cwd()
    project_root = Path(project_root)

    src_dir = project_root / "src"
    if not src_dir.exists():
        return FormatResult(
            success=False,
            errors=[f"Répertoire src introuvable: {src_dir}"],
        )

    typ_files = list(src_dir.rglob("*.typ"))
    if not typ_files:
        return FormatResult(
            success=False,
            errors=["Aucun fichier .typ trouvé dans src/"],
        )

    content = ValidatedContent(collect_typ_content(src_dir))

    ctx = (
        FormatContext(content=content, result=FormatResult(success=True))
        .map(step_fill_statistics)
        .map(step_verify_sections)
        .bind(step_verify_contact)
        .map(step_verify_entries)
        .map(step_verify_whitespace)
        .bind(step_verify_encoding)
        .map(step_verify_french_chars)
    )

    return ctx.result


def print_result(result: FormatResult) -> None:
    print("=== Vérification du formatage ===")
    print()

    print("1. Vérification des espaces...")
    ws_warnings = [w for w in result.warnings if "espaces en fin" in w]
    for w in ws_warnings:
        print(f"  ATTENTION: {w}")
    if not ws_warnings:
        print("  OK: Pas d'espaces en fin de ligne")

    print()
    print("2. Vérification de la structure...")
    for section in REQUIRED_SECTIONS:
        if section in result.sections_found:
            print(f"  OK: Section '{section}' présente")
        else:
            print(f"  ATTENTION: Section '{section}' manquante")

    print()
    print("3. Vérification des informations de contact...")
    for item in ["email", "phone", "linkedin"]:
        errors_for_item = [e for e in result.errors if item in e.lower()]
        warnings_for_item = [w for w in result.warnings if item in w.lower()]
        if errors_for_item:
            print(f"  ERREUR: {errors_for_item[0]}")
        elif warnings_for_item:
            print(f"  ATTENTION: {warnings_for_item[0]}")
        else:
            print(f"  OK: {item.capitalize()} présent")

    print()
    print("4. Vérification des entrées...")
    print(f"  Nombre d'entrées (#entry): {result.entry_count}")
    if result.entry_count < 5:
        print("  ATTENTION: Peu d'entrées dans le CV")

    print()
    print("5. Vérification des caractères spéciaux...")
    encoding_errors = [e for e in result.errors if "encodage" in e.lower()]
    if encoding_errors:
        print(f"  ERREUR: {encoding_errors[0]}")
    else:
        print("  OK: Pas de problème d'encodage")

    french_warnings = [w for w in result.warnings if "accentués" in w.lower()]
    if french_warnings:
        print(f"  ATTENTION: {french_warnings[0]}")
    else:
        print("  OK: Caractères français présents")

    print()
    print("6. Statistiques du fichier...")
    print(f"  Lignes: {result.line_count}")
    print(f"  Caractères: {result.char_count}")

    print()
    print("=== Résumé ===")
    print(f"Erreurs: {len(result.errors)}")
    print(f"Avertissements: {len(result.warnings)}")

    print()
    if result.success:
        print("=== Vérification du formatage: RÉUSSIE ===")
    else:
        print("=== Vérification du formatage: ÉCHEC ===")


if __name__ == "__main__":
    import sys

    current = Path.cwd()
    while current != current.parent:
        if (current / "src").is_dir():
            break
        current = current.parent
    else:
        current = Path.cwd()

    result = verify_format(current)
    print_result(result)
    sys.exit(0 if result.success else 1)
