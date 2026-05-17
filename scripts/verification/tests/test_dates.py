from pathlib import Path

from scripts.lib import ValidatedContent
from scripts.verification.dates import (
    DateInfo,
    DatesContext,
    DatesResult,
    extract_all_dates,
    extract_dates_from_line,
    is_comment_line,
    step_check_future_dates,
    step_check_old_dates,
    step_count_formats,
    step_extract_dates,
    verify_dates,
)


def make_context(content: str, current_year: int = 2025) -> DatesContext:
    return DatesContext(
        content=ValidatedContent(content),
        result=DatesResult(success=True),
        current_year=current_year,
    )


class TestExtractDatesFromLine:
    def test_mm_yyyy_format(self):
        dates = extract_dates_from_line('date: "02/2021 - 10/2025"', 1)
        assert len(dates) == 2
        assert dates[0].year == 2021
        assert dates[0].month == 2
        assert dates[1].year == 2025
        assert dates[1].month == 10

    def test_yyyy_only_format(self):
        dates = extract_dates_from_line('date: "2022"', 1)
        assert len(dates) == 1
        assert dates[0].year == 2022
        assert dates[0].month is None

    def test_invalid_month_falls_back_to_year(self):
        dates = extract_dates_from_line('date: "13/2021"', 1)
        assert len(dates) == 1
        assert dates[0].year == 2021

    def test_no_dates(self):
        dates = extract_dates_from_line("title: Senior Developer", 1)
        assert len(dates) == 0

    def test_line_number_stored(self):
        dates = extract_dates_from_line('date: "2020"', 42)
        assert dates[0].line_number == 42


class TestIsCommentLine:
    def test_comment_line(self):
        assert is_comment_line("// This is a comment") is True
        assert is_comment_line("  // Indented comment") is True

    def test_not_comment_line(self):
        assert is_comment_line("date: 2021") is False
        assert is_comment_line("") is False


class TestExtractAllDates:
    def test_extracts_from_cv_content(self):
        content = """
#entry(
  title: "Developer",
  date: "02/2021 - 10/2025",
)
// date: "commented out"
#entry(
  title: "Education",
  date: "2020",
)
"""
        dates = extract_all_dates(content)
        assert len(dates) >= 2

    def test_skips_comments(self):
        content = """
// date: "01/2020 - 12/2020"
date: "01/2021"
"""
        dates = extract_all_dates(content)
        assert len(dates) == 1
        assert dates[0].year == 2021


class TestStepExtractDates:
    def test_populates_dates_found(self):
        ctx = make_context('date: "02/2021"\ndate: "2022"')
        result = step_extract_dates(ctx)
        assert len(result.result.dates_found) == 2


class TestStepCheckFutureDates:
    def test_no_errors_when_no_future_dates(self):
        ctx = make_context("")
        ctx.result.dates_found = [
            DateInfo(year=2020, line_number=1, line_content=""),
            DateInfo(year=2023, line_number=2, line_content=""),
        ]
        ctx.current_year = 2025
        result = step_check_future_dates(ctx)
        assert len(result.result.errors) == 0
        assert result.result.success is True

    def test_error_when_future_date_found(self):
        ctx = make_context("")
        ctx.result.dates_found = [
            DateInfo(year=2025, line_number=1, line_content=""),
            DateInfo(year=2030, line_number=2, line_content=""),
        ]
        ctx.current_year = 2025
        result = step_check_future_dates(ctx)
        assert len(result.result.errors) == 1
        assert "2030" in result.result.errors[0]
        assert result.result.success is False


class TestStepCheckOldDates:
    def test_no_warnings_when_no_old_dates(self):
        ctx = make_context("")
        ctx.result.dates_found = [
            DateInfo(year=2000, line_number=1, line_content="date: 2000"),
            DateInfo(year=2020, line_number=2, line_content="date: 2020"),
        ]
        result = step_check_old_dates(ctx)
        assert len(result.result.warnings) == 0

    def test_warning_when_old_date_found(self):
        ctx = make_context("")
        ctx.result.dates_found = [
            DateInfo(year=1985, line_number=1, line_content="date: 1985"),
        ]
        result = step_check_old_dates(ctx)
        assert len(result.result.warnings) == 1
        assert "1985" in result.result.warnings[0]

    def test_skips_birth_date(self):
        ctx = make_context("")
        ctx.result.dates_found = [
            DateInfo(
                year=1979,
                line_number=1,
                line_content="Date de naissance : 3/03/1979",
            ),
        ]
        result = step_check_old_dates(ctx)
        assert len(result.result.warnings) == 0


class TestStepCountFormats:
    def test_counts_formats(self):
        content = """
date: "02/2021 - 10/2025",
date: "2022",
date: "01/2020 - Aujourd'hui",
// date: "ignored"
"""
        ctx = make_context(content)
        result = step_count_formats(ctx)
        assert result.result.format_stats["mm_yyyy"] >= 1
        assert result.result.format_stats["yyyy_only"] >= 1
        assert result.result.format_stats["aujourdhui"] >= 1


class TestDatesContext:
    def test_bind_executes_on_success(self):
        ctx = make_context("")

        def add_warning(c: DatesContext) -> DatesContext:
            c.result.warnings.append("test")
            return c

        result = ctx.bind(add_warning)
        assert "test" in result.result.warnings

    def test_bind_short_circuits_on_failure(self):
        ctx = make_context("")
        ctx.result.success = False

        def should_not_run(c: DatesContext) -> DatesContext:
            c.result.warnings.append("should not appear")
            return c

        result = ctx.bind(should_not_run)
        assert "should not appear" not in result.result.warnings

    def test_map_always_executes(self):
        ctx = make_context("")
        ctx.result.success = False

        def add_warning(c: DatesContext) -> DatesContext:
            c.result.warnings.append("executed")
            return c

        result = ctx.map(add_warning)
        assert "executed" in result.result.warnings


class TestVerifyDates:
    def test_success(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text('date: "02/2021 - 10/2025",\ndate: "2020",')

        result = verify_dates(tmp_path)
        assert result.success is True
        assert len(result.errors) == 0

    def test_failure_future_date(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text('date: "2050"')

        result = verify_dates(tmp_path)
        assert result.success is False
        assert any("future" in e.lower() for e in result.errors)

    def test_failure_no_file(self, tmp_path: Path):
        result = verify_dates(tmp_path)
        assert result.success is False
        assert any("introuvable" in e.lower() for e in result.errors)

    def test_pipeline_short_circuits(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text('date: "2050"\ndate: "1980"')

        result = verify_dates(tmp_path)
        assert result.success is False
        assert any("future" in e.lower() for e in result.errors)


class TestDatesResult:
    def test_default_values(self):
        result = DatesResult(success=True)
        assert result.success is True
        assert result.errors == []
        assert result.warnings == []
        assert result.dates_found == []
        assert result.format_stats == {}


class TestDateInfo:
    def test_frozen(self):
        date_info = DateInfo(year=2021, month=2, line_number=1, line_content="test")
        assert date_info.year == 2021

    def test_default_values(self):
        date_info = DateInfo(year=2021)
        assert date_info.month is None
        assert date_info.line_number == 0
        assert date_info.line_content == ""
