from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.lib import ProjectRoot
from scripts.verification.runner import (
    AllVerificationsResult,
    RunnerContext,
    RunnerResult,
    run_all_verifications,
    step_aggregate_results,
    step_print_header,
    step_print_summary,
    step_run_build,
    step_run_dates,
    step_run_format,
)


def make_context(tmp_path: Path, verbose: bool = False) -> RunnerContext:
    (tmp_path / "src").mkdir(parents=True, exist_ok=True)
    (tmp_path / "src" / "cv.typ").touch()
    return RunnerContext(
        project_root=ProjectRoot(tmp_path),
        result=RunnerResult(success=True),
        verbose=verbose,
    )


class TestRunnerContext:
    def test_bind_executes_on_success(self, tmp_path: Path):
        ctx = make_context(tmp_path)

        def add_check(c: RunnerContext) -> RunnerContext:
            c.result.failed_checks.append("test")
            return c

        result = ctx.bind(add_check)
        assert "test" in result.result.failed_checks

    def test_bind_short_circuits_on_failure(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        ctx.result.success = False

        def should_not_run(c: RunnerContext) -> RunnerContext:
            c.result.failed_checks.append("should not appear")
            return c

        result = ctx.bind(should_not_run)
        assert "should not appear" not in result.result.failed_checks

    def test_map_always_executes(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        ctx.result.success = False

        def add_check(c: RunnerContext) -> RunnerContext:
            c.result.failed_checks.append("executed")
            return c

        result = ctx.map(add_check)
        assert "executed" in result.result.failed_checks


class TestStepPrintHeader:
    def test_prints_when_verbose(self, tmp_path: Path, capsys):
        ctx = make_context(tmp_path, verbose=True)
        step_print_header(ctx)
        captured = capsys.readouterr()
        assert "VÉRIFICATION COMPLÈTE DU CV" in captured.out

    def test_silent_when_not_verbose(self, tmp_path: Path, capsys):
        ctx = make_context(tmp_path, verbose=False)
        step_print_header(ctx)
        captured = capsys.readouterr()
        assert captured.out == ""


class TestStepRunBuild:
    def test_records_failure(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        mock_result = MagicMock()
        mock_result.success = False

        with patch(
            "scripts.verification.runner.verify_build", return_value=mock_result
        ):
            result = step_run_build(ctx)

        assert "build" in result.result.failed_checks
        assert result.result.build_result == mock_result

    def test_records_success(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        mock_result = MagicMock()
        mock_result.success = True

        with patch(
            "scripts.verification.runner.verify_build", return_value=mock_result
        ):
            result = step_run_build(ctx)

        assert "build" not in result.result.failed_checks


class TestStepRunDates:
    def test_records_failure(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        mock_result = MagicMock()
        mock_result.success = False

        with patch(
            "scripts.verification.runner.verify_dates", return_value=mock_result
        ):
            result = step_run_dates(ctx)

        assert "dates" in result.result.failed_checks
        assert result.result.dates_result == mock_result

    def test_records_success(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        mock_result = MagicMock()
        mock_result.success = True

        with patch(
            "scripts.verification.runner.verify_dates", return_value=mock_result
        ):
            result = step_run_dates(ctx)

        assert "dates" not in result.result.failed_checks


class TestStepRunFormat:
    def test_records_failure(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        mock_result = MagicMock()
        mock_result.success = False

        with patch(
            "scripts.verification.runner.verify_format", return_value=mock_result
        ):
            result = step_run_format(ctx)

        assert "format" in result.result.failed_checks
        assert result.result.format_result == mock_result

    def test_records_success(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        mock_result = MagicMock()
        mock_result.success = True

        with patch(
            "scripts.verification.runner.verify_format", return_value=mock_result
        ):
            result = step_run_format(ctx)

        assert "format" not in result.result.failed_checks


class TestStepAggregateResults:
    def test_success_when_no_failures(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        ctx.result.failed_checks = []
        result = step_aggregate_results(ctx)
        assert result.result.success is True

    def test_failure_when_has_failures(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        ctx.result.failed_checks = ["build", "dates"]
        result = step_aggregate_results(ctx)
        assert result.result.success is False


class TestStepPrintSummary:
    def test_prints_success_when_verbose(self, tmp_path: Path, capsys):
        ctx = make_context(tmp_path, verbose=True)
        ctx.result.success = True
        step_print_summary(ctx)
        captured = capsys.readouterr()
        assert "Toutes les vérifications ont réussi" in captured.out

    def test_prints_failures_when_verbose(self, tmp_path: Path, capsys):
        ctx = make_context(tmp_path, verbose=True)
        ctx.result.success = False
        ctx.result.failed_checks = ["build", "dates"]
        step_print_summary(ctx)
        captured = capsys.readouterr()
        assert "ÉCHEC" in captured.out
        assert "build" in captured.out
        assert "dates" in captured.out

    def test_silent_when_not_verbose(self, tmp_path: Path, capsys):
        ctx = make_context(tmp_path, verbose=False)
        step_print_summary(ctx)
        captured = capsys.readouterr()
        assert captured.out == ""


class TestRunAllVerifications:
    def test_invalid_project_root(self, tmp_path: Path):
        result = run_all_verifications(tmp_path, verbose=False)
        assert result.success is False
        assert "project_root" in result.failed_checks

    def test_runs_all_checks(self, tmp_path: Path):
        (tmp_path / "src").mkdir(parents=True)
        (tmp_path / "src" / "cv.typ").touch()

        mock_build = MagicMock(success=True)
        mock_dates = MagicMock(success=True)
        mock_format = MagicMock(success=True)

        with (
            patch(
                "scripts.verification.runner.verify_build", return_value=mock_build
            ),
            patch(
                "scripts.verification.runner.verify_dates", return_value=mock_dates
            ),
            patch(
                "scripts.verification.runner.verify_format", return_value=mock_format
            ),
        ):
            result = run_all_verifications(tmp_path, verbose=False)

        assert result.success is True
        assert result.build_result == mock_build
        assert result.dates_result == mock_dates
        assert result.format_result == mock_format

    def test_collects_all_failures(self, tmp_path: Path):
        (tmp_path / "src").mkdir(parents=True)
        (tmp_path / "src" / "cv.typ").touch()

        mock_build = MagicMock(success=False)
        mock_dates = MagicMock(success=False)
        mock_format = MagicMock(success=True)

        with (
            patch(
                "scripts.verification.runner.verify_build", return_value=mock_build
            ),
            patch(
                "scripts.verification.runner.verify_dates", return_value=mock_dates
            ),
            patch(
                "scripts.verification.runner.verify_format", return_value=mock_format
            ),
        ):
            result = run_all_verifications(tmp_path, verbose=False)

        assert result.success is False
        assert "build" in result.failed_checks
        assert "dates" in result.failed_checks
        assert "format" not in result.failed_checks


class TestRunnerResult:
    def test_default_values(self):
        result = RunnerResult(success=True)
        assert result.success is True
        assert result.build_result is None
        assert result.dates_result is None
        assert result.format_result is None
        assert result.failed_checks == []


class TestBackwardCompatibility:
    def test_alias_exists(self):
        assert AllVerificationsResult is RunnerResult
