import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Callable

from scripts.lib import ValidatedContent

MM_YYYY_PATTERN = re.compile(r"\b(\d{1,2})/(\d{4})\b")
YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")


@dataclass(frozen=True)
class DateInfo:
    year: int
    month: int | None = None
    line_number: int = 0
    line_content: str = ""


@dataclass
class DatesResult:
    success: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    dates_found: list[DateInfo] = field(default_factory=list)
    format_stats: dict[str, int] = field(default_factory=dict)


DatesStep = Callable[["DatesContext"], "DatesContext"]


@dataclass
class DatesContext:
    content: ValidatedContent
    result: DatesResult
    current_year: int = field(default_factory=lambda: date.today().year)

    def bind(self, func: DatesStep) -> "DatesContext":
        if not self.result.success:
            return self
        return func(self)

    def map(self, func: DatesStep) -> "DatesContext":
        return func(self)


def is_comment_line(line: str) -> bool:
    return line.strip().startswith("//")


def extract_dates_from_line(line: str, line_number: int) -> list[DateInfo]:
    dates = []

    for match in MM_YYYY_PATTERN.finditer(line):
        month = int(match.group(1))
        year = int(match.group(2))
        if 1 <= month <= 12:
            dates.append(
                DateInfo(
                    year=year,
                    month=month,
                    line_number=line_number,
                    line_content=line.strip(),
                )
            )

    if not dates:
        for match in YEAR_PATTERN.finditer(line):
            year = int(match.group(0))
            dates.append(
                DateInfo(
                    year=year,
                    month=None,
                    line_number=line_number,
                    line_content=line.strip(),
                )
            )

    return dates


def extract_all_dates(content: str) -> list[DateInfo]:
    all_dates = []

    for i, line in enumerate(content.split("\n"), start=1):
        if is_comment_line(line):
            continue
        if "date:" in line.lower() or "Date" in line:
            dates = extract_dates_from_line(line, i)
            all_dates.extend(dates)

    return all_dates


def step_extract_dates(ctx: DatesContext) -> DatesContext:
    ctx.result.dates_found = extract_all_dates(ctx.content)
    return ctx


def step_check_future_dates(ctx: DatesContext) -> DatesContext:
    for date_info in ctx.result.dates_found:
        if date_info.year > ctx.current_year:
            ctx.result.errors.append(
                f"Année future détectée: {date_info.year} (ligne {date_info.line_number})"
            )
            ctx.result.success = False
    return ctx


def step_check_old_dates(ctx: DatesContext, threshold_year: int = 1990) -> DatesContext:
    for date_info in ctx.result.dates_found:
        if "naissance" in date_info.line_content.lower():
            continue
        if date_info.year < threshold_year:
            ctx.result.warnings.append(
                f"Année très ancienne: {date_info.year} (ligne {date_info.line_number})"
            )
    return ctx


def step_count_formats(ctx: DatesContext) -> DatesContext:
    stats = {"mm_yyyy": 0, "yyyy_only": 0, "aujourdhui": 0, "present": 0}

    for line in ctx.content.split("\n"):
        if is_comment_line(line):
            continue
        if "date:" not in line.lower():
            continue

        if MM_YYYY_PATTERN.search(line):
            stats["mm_yyyy"] += 1
        elif YEAR_PATTERN.search(line):
            stats["yyyy_only"] += 1

        if "aujourd" in line.lower():
            stats["aujourdhui"] += 1
        if "présent" in line.lower() or "present" in line.lower():
            stats["present"] += 1

    ctx.result.format_stats = stats
    return ctx


def verify_dates(project_root: Path | None = None) -> DatesResult:
    if project_root is None:
        project_root = Path.cwd()
    project_root = Path(project_root)

    cv_file = project_root / "src" / "cv.typ"
    if not cv_file.exists():
        return DatesResult(
            success=False,
            errors=[f"Fichier CV introuvable: {cv_file}"],
        )

    content = ValidatedContent(cv_file.read_text(encoding="utf-8"))

    ctx = (
        DatesContext(content=content, result=DatesResult(success=True))
        .map(step_extract_dates)
        .bind(step_check_future_dates)
        .map(step_check_old_dates)
        .map(step_count_formats)
    )

    return ctx.result


def print_result(result: DatesResult) -> None:
    print("=== Vérification des dates ===")
    print()

    current_year = date.today().year
    print(f"Année courante: {current_year}")
    print()

    print("Analyse des dates...")

    if result.errors:
        for error in result.errors:
            print(f"ERREUR: {error}")

    if result.warnings:
        for warning in result.warnings:
            print(f"ATTENTION: {warning}")

    print()
    print("Vérification du format des dates...")
    if result.format_stats:
        print(f"  Format MM/YYYY: {result.format_stats.get('mm_yyyy', 0)} occurrences")
        print(f"  Format YYYY seul: {result.format_stats.get('yyyy_only', 0)} occurrences")
        aujourdhui = result.format_stats.get("aujourdhui", 0)
        present = result.format_stats.get("present", 0)
        print(f"  Avec 'Aujourd'hui'/'Présent': {aujourdhui + present} occurrences")

    print()
    print("=== Résumé ===")
    print(f"Erreurs: {len(result.errors)}")
    print(f"Avertissements: {len(result.warnings)}")

    print()
    if result.success:
        print("=== Vérification des dates: RÉUSSIE ===")
    else:
        print("=== Vérification des dates: ÉCHEC ===")


if __name__ == "__main__":
    import sys

    current = Path.cwd()
    while current != current.parent:
        if (current / "src" / "cv.typ").exists():
            break
        current = current.parent
    else:
        current = Path.cwd()

    result = verify_dates(current)
    print_result(result)
    sys.exit(0 if result.success else 1)
