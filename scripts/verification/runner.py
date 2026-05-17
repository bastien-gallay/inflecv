from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from scripts.lib import ProjectRoot, is_valid_project_root

from .build import BuildResult, print_result as print_build_result, verify_build
from .dates import DatesResult, print_result as print_dates_result, verify_dates
from .format import FormatResult, print_result as print_format_result, verify_format


@dataclass
class RunnerResult:
    success: bool
    build_result: BuildResult | None = None
    dates_result: DatesResult | None = None
    format_result: FormatResult | None = None
    failed_checks: list[str] = field(default_factory=list)


RunnerStep = Callable[["RunnerContext"], "RunnerContext"]


@dataclass
class RunnerContext:
    project_root: ProjectRoot
    result: RunnerResult
    verbose: bool = True

    def bind(self, func: RunnerStep) -> "RunnerContext":
        if not self.result.success:
            return self
        return func(self)

    def map(self, func: RunnerStep) -> "RunnerContext":
        return func(self)


def step_print_header(ctx: RunnerContext) -> RunnerContext:
    if ctx.verbose:
        print("=" * 42)
        print("     VÉRIFICATION COMPLÈTE DU CV")
        print("=" * 42)
        print()
    return ctx


def step_run_build(ctx: RunnerContext) -> RunnerContext:
    if ctx.verbose:
        print("-" * 42)
    ctx.result.build_result = verify_build(ctx.project_root)
    if ctx.verbose:
        print_build_result(ctx.result.build_result)
    if not ctx.result.build_result.success:
        ctx.result.failed_checks.append("build")
    return ctx


def step_run_dates(ctx: RunnerContext) -> RunnerContext:
    if ctx.verbose:
        print()
        print("-" * 42)
    ctx.result.dates_result = verify_dates(ctx.project_root)
    if ctx.verbose:
        print_dates_result(ctx.result.dates_result)
    if not ctx.result.dates_result.success:
        ctx.result.failed_checks.append("dates")
    return ctx


def step_run_format(ctx: RunnerContext) -> RunnerContext:
    if ctx.verbose:
        print()
        print("-" * 42)
    ctx.result.format_result = verify_format(ctx.project_root)
    if ctx.verbose:
        print_format_result(ctx.result.format_result)
    if not ctx.result.format_result.success:
        ctx.result.failed_checks.append("format")
    return ctx


def step_aggregate_results(ctx: RunnerContext) -> RunnerContext:
    ctx.result.success = len(ctx.result.failed_checks) == 0
    return ctx


def step_print_summary(ctx: RunnerContext) -> RunnerContext:
    if not ctx.verbose:
        return ctx

    print()
    print("=" * 42)
    print("     RÉSUMÉ FINAL")
    print("=" * 42)
    print()

    if ctx.result.success:
        print("Toutes les vérifications ont réussi!")
        print()
        print("Checklist manuelle: voir VERIFICATION.md")
    else:
        print(f"ÉCHEC: {len(ctx.result.failed_checks)} vérification(s) ont échoué")
        for check in ctx.result.failed_checks:
            print(f"  - {check}")
        print()
        print("Corrigez les erreurs et relancez la vérification.")

    print()
    return ctx


def run_all_verifications(
    project_root: Path | None = None,
    verbose: bool = True,
) -> RunnerResult:
    if project_root is None:
        project_root = Path.cwd()
    project_root = Path(project_root)

    if not is_valid_project_root(project_root):
        result = RunnerResult(success=False)
        result.failed_checks.append("project_root")
        if verbose:
            print(f"Racine de projet invalide: {project_root}")
        return result

    ctx = (
        RunnerContext(
            project_root=ProjectRoot(project_root),
            result=RunnerResult(success=True),
            verbose=verbose,
        )
        .map(step_print_header)
        .map(step_run_build)
        .map(step_run_dates)
        .map(step_run_format)
        .map(step_aggregate_results)
        .map(step_print_summary)
    )

    return ctx.result


# Backward compatibility alias
AllVerificationsResult = RunnerResult
