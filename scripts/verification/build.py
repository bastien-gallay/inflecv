import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from scripts.lib import ProjectRoot, is_valid_project_root

BuildStep = Callable[["BuildContext"], "BuildContext"]


@dataclass
class BuildResult:
    success: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    pdf_path: Path | None = None
    pdf_size: int = 0


@dataclass
class BuildContext:
    project_root: ProjectRoot
    result: BuildResult
    compile_stderr: str = ""

    def bind(self, func: "BuildStep") -> "BuildContext":
        if not self.result.success:
            return self
        return func(self)

    def map(self, func: "BuildStep") -> "BuildContext":
        return func(self)


def step_check_typst(ctx: BuildContext) -> BuildContext:
    if shutil.which("typst") is None:
        ctx.result.errors.append("typst n'est pas installé ou pas dans le PATH")
        ctx.result.success = False
    return ctx


def step_check_source(ctx: BuildContext) -> BuildContext:
    cv_file = ctx.project_root / "src" / "cv.typ"
    if not cv_file.exists():
        ctx.result.errors.append(f"Fichier source introuvable: {cv_file}")
        ctx.result.success = False
    return ctx


def step_compile(ctx: BuildContext) -> BuildContext:
    cv_file = ctx.project_root / "src" / "cv.typ"
    dist_dir = ctx.project_root / "dist"
    dist_dir.mkdir(exist_ok=True)
    pdf_path = dist_dir / "cv.pdf"

    result = subprocess.run(
        ["typst", "compile", str(cv_file), str(pdf_path)],
        capture_output=True,
        text=True,
    )

    ctx.compile_stderr = result.stderr
    if result.returncode != 0:
        ctx.result.errors.append(f"Échec de la compilation: {result.stderr}")
        ctx.result.success = False
    return ctx


def step_parse_warnings(ctx: BuildContext) -> BuildContext:
    if ctx.compile_stderr:
        for line in ctx.compile_stderr.split("\n"):
            if "warning:" in line.lower():
                ctx.result.warnings.append(line.strip())
    return ctx


def step_validate_pdf(ctx: BuildContext) -> BuildContext:
    pdf_path = ctx.project_root / "dist" / "cv.pdf"

    if not pdf_path.exists():
        ctx.result.errors.append("Le PDF n'a pas été généré")
        ctx.result.success = False
        return ctx

    size = pdf_path.stat().st_size
    if size == 0:
        ctx.result.errors.append("Le PDF est vide")
        ctx.result.success = False
        return ctx

    ctx.result.pdf_path = pdf_path
    ctx.result.pdf_size = size
    return ctx


def verify_build(project_root: Path | None = None) -> BuildResult:
    if project_root is None:
        project_root = Path.cwd()
    project_root = Path(project_root)

    if not is_valid_project_root(project_root):
        return BuildResult(
            success=False,
            errors=[f"Racine projet invalide: {project_root}"],
        )

    ctx = (
        BuildContext(
            project_root=ProjectRoot(project_root),
            result=BuildResult(success=True),
        )
        .bind(step_check_typst)
        .bind(step_check_source)
        .bind(step_compile)
        .map(step_parse_warnings)
        .bind(step_validate_pdf)
    )

    return ctx.result


def print_result(result: BuildResult) -> None:
    print("=== Vérification de la compilation ===")
    print()

    if result.errors:
        for error in result.errors:
            print(f"ERREUR: {error}")
        print()
        print("=== Vérification de la compilation: ÉCHEC ===")
        return

    print("OK: Compilation réussie")

    if result.warnings:
        print()
        print("Avertissements:")
        for warning in result.warnings:
            print(f"  {warning}")

    if result.pdf_path:
        print(f"OK: PDF généré ({result.pdf_size} octets)")

    print()
    print("=== Vérification de la compilation: RÉUSSIE ===")


if __name__ == "__main__":
    import sys

    current = Path.cwd()
    while current != current.parent:
        if (current / "src" / "cv.typ").exists():
            break
        current = current.parent
    else:
        current = Path.cwd()

    result = verify_build(current)
    print_result(result)
    sys.exit(0 if result.success else 1)
