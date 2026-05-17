import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.lib import ProjectRoot
from scripts.verification.build import (
    BuildContext,
    BuildResult,
    step_check_source,
    step_check_typst,
    step_compile,
    step_parse_warnings,
    step_validate_pdf,
    verify_build,
)


def make_context(tmp_path: Path) -> BuildContext:
    (tmp_path / "src").mkdir(parents=True, exist_ok=True)
    (tmp_path / "src" / "cv.typ").touch()
    return BuildContext(
        project_root=ProjectRoot(tmp_path),
        result=BuildResult(success=True),
    )


class TestStepCheckTypst:
    def test_success_when_installed(self):
        ctx = BuildContext(
            project_root=ProjectRoot(Path("/tmp")),
            result=BuildResult(success=True),
        )
        with patch.object(shutil, "which", return_value="/usr/bin/typst"):
            result = step_check_typst(ctx)
        assert result.result.success is True
        assert len(result.result.errors) == 0

    def test_failure_when_not_installed(self):
        ctx = BuildContext(
            project_root=ProjectRoot(Path("/tmp")),
            result=BuildResult(success=True),
        )
        with patch.object(shutil, "which", return_value=None):
            result = step_check_typst(ctx)
        assert result.result.success is False
        assert any("typst" in e.lower() for e in result.result.errors)


class TestStepCheckSource:
    def test_success_when_exists(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        result = step_check_source(ctx)
        assert result.result.success is True

    def test_failure_when_missing(self, tmp_path: Path):
        ctx = BuildContext(
            project_root=ProjectRoot(tmp_path),
            result=BuildResult(success=True),
        )
        result = step_check_source(ctx)
        assert result.result.success is False
        assert any("introuvable" in e.lower() for e in result.result.errors)


class TestStepCompile:
    def test_success(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""

        with patch("subprocess.run", return_value=mock_result):
            result = step_compile(ctx)
        assert result.result.success is True

    def test_failure(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "error: syntax error"

        with patch("subprocess.run", return_value=mock_result):
            result = step_compile(ctx)
        assert result.result.success is False
        assert any("compilation" in e.lower() for e in result.result.errors)


class TestStepParseWarnings:
    def test_extracts_warnings(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        ctx.compile_stderr = "warning: unused variable\ninfo: something\nwarning: another"
        result = step_parse_warnings(ctx)
        assert len(result.result.warnings) == 2

    def test_no_warnings_when_empty(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        ctx.compile_stderr = ""
        result = step_parse_warnings(ctx)
        assert len(result.result.warnings) == 0


class TestStepValidatePdf:
    def test_success_when_valid(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        pdf_path = tmp_path / "dist" / "cv.pdf"
        pdf_path.parent.mkdir(parents=True)
        pdf_path.write_bytes(b"%PDF-1.4 dummy content")

        result = step_validate_pdf(ctx)
        assert result.result.success is True
        assert result.result.pdf_size > 0
        assert result.result.pdf_path == pdf_path

    def test_failure_when_missing(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        result = step_validate_pdf(ctx)
        assert result.result.success is False
        assert any("généré" in e.lower() for e in result.result.errors)

    def test_failure_when_empty(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        pdf_path = tmp_path / "dist" / "cv.pdf"
        pdf_path.parent.mkdir(parents=True)
        pdf_path.write_bytes(b"")

        result = step_validate_pdf(ctx)
        assert result.result.success is False
        assert any("vide" in e.lower() for e in result.result.errors)


class TestBuildContext:
    def test_bind_executes_on_success(self, tmp_path: Path):
        ctx = make_context(tmp_path)

        def add_warning(c: BuildContext) -> BuildContext:
            c.result.warnings.append("test")
            return c

        result = ctx.bind(add_warning)
        assert "test" in result.result.warnings

    def test_bind_short_circuits_on_failure(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        ctx.result.success = False

        def should_not_run(c: BuildContext) -> BuildContext:
            c.result.warnings.append("should not appear")
            return c

        result = ctx.bind(should_not_run)
        assert "should not appear" not in result.result.warnings

    def test_map_always_executes(self, tmp_path: Path):
        ctx = make_context(tmp_path)
        ctx.result.success = False

        def add_warning(c: BuildContext) -> BuildContext:
            c.result.warnings.append("executed")
            return c

        result = ctx.map(add_warning)
        assert "executed" in result.result.warnings


class TestVerifyBuild:
    def test_success(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text("// CV content")

        pdf_path = tmp_path / "dist" / "cv.pdf"
        pdf_path.parent.mkdir(parents=True)
        pdf_path.write_bytes(b"%PDF-1.4 dummy")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""

        with (
            patch.object(shutil, "which", return_value="/usr/bin/typst"),
            patch("subprocess.run", return_value=mock_result),
        ):
            result = verify_build(tmp_path)

        assert result.success is True
        assert len(result.errors) == 0
        assert result.pdf_size > 0

    def test_failure_no_typst(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text("// CV content")

        with patch.object(shutil, "which", return_value=None):
            result = verify_build(tmp_path)

        assert result.success is False
        assert any("typst" in e.lower() for e in result.errors)

    def test_failure_invalid_project_root(self, tmp_path: Path):
        result = verify_build(tmp_path)
        assert result.success is False
        assert any("invalide" in e.lower() for e in result.errors)

    def test_pipeline_short_circuits(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text("// CV content")

        with patch.object(shutil, "which", return_value=None):
            result = verify_build(tmp_path)

        assert result.success is False
        assert not any("compilation" in e.lower() for e in result.errors)


class TestBuildResult:
    def test_default_values(self):
        result = BuildResult(success=True)
        assert result.success is True
        assert result.errors == []
        assert result.warnings == []
        assert result.pdf_path is None
        assert result.pdf_size == 0

    def test_with_errors(self):
        result = BuildResult(success=False, errors=["Error 1", "Error 2"])
        assert result.success is False
        assert len(result.errors) == 2
