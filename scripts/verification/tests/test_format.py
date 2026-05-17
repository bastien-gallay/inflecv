from pathlib import Path

from scripts.lib import ValidatedContent
from scripts.verification.format import (
    FormatContext,
    FormatResult,
    check_contact_info,
    check_encoding_errors,
    check_french_chars,
    check_sections,
    check_trailing_whitespace,
    count_entries,
    step_fill_statistics,
    step_verify_contact,
    step_verify_encoding,
    step_verify_entries,
    step_verify_french_chars,
    step_verify_sections,
    step_verify_whitespace,
    verify_format,
)


def make_context(content: str) -> FormatContext:
    return FormatContext(
        content=ValidatedContent(content),
        result=FormatResult(success=True),
    )


class TestFormatContext:
    def test_map_always_executes(self):
        ctx = make_context("test")

        def add_warning(c: FormatContext) -> FormatContext:
            c.result.warnings.append("test warning")
            return c

        result = ctx.map(add_warning)
        assert "test warning" in result.result.warnings

    def test_map_executes_even_on_failure(self):
        ctx = make_context("test")
        ctx.result.success = False

        def add_warning(c: FormatContext) -> FormatContext:
            c.result.warnings.append("executed")
            return c

        result = ctx.map(add_warning)
        assert "executed" in result.result.warnings

    def test_bind_executes_on_success(self):
        ctx = make_context("test")

        def add_error(c: FormatContext) -> FormatContext:
            c.result.errors.append("new error")
            return c

        result = ctx.bind(add_error)
        assert "new error" in result.result.errors

    def test_bind_short_circuits_on_failure(self):
        ctx = make_context("test")
        ctx.result.success = False
        ctx.result.errors.append("previous error")

        def add_error(c: FormatContext) -> FormatContext:
            c.result.errors.append("should not appear")
            return c

        result = ctx.bind(add_error)
        assert "should not appear" not in result.result.errors
        assert len(result.result.errors) == 1

    def test_chaining_map_operations(self):
        ctx = make_context("test content")

        def step1(c: FormatContext) -> FormatContext:
            c.result.warnings.append("step1")
            return c

        def step2(c: FormatContext) -> FormatContext:
            c.result.warnings.append("step2")
            return c

        def step3(c: FormatContext) -> FormatContext:
            c.result.warnings.append("step3")
            return c

        result = ctx.map(step1).map(step2).map(step3)
        assert result.result.warnings == ["step1", "step2", "step3"]

    def test_chaining_bind_short_circuits_after_failure(self):
        ctx = make_context("test")

        def fail_step(c: FormatContext) -> FormatContext:
            c.result.errors.append("critical failure")
            c.result.success = False
            return c

        def should_not_run(c: FormatContext) -> FormatContext:
            c.result.errors.append("should not appear")
            return c

        result = ctx.bind(fail_step).bind(should_not_run)
        assert "critical failure" in result.result.errors
        assert "should not appear" not in result.result.errors

    def test_mixed_map_and_bind(self):
        ctx = make_context("test")

        def warn_step(c: FormatContext) -> FormatContext:
            c.result.warnings.append("warning")
            return c

        def fail_step(c: FormatContext) -> FormatContext:
            c.result.errors.append("error")
            c.result.success = False
            return c

        def final_warn(c: FormatContext) -> FormatContext:
            c.result.warnings.append("final")
            return c

        result = ctx.map(warn_step).bind(fail_step).map(final_warn)
        assert "warning" in result.result.warnings
        assert "error" in result.result.errors
        assert "final" in result.result.warnings


class TestStepFillStatistics:
    def test_counts_lines(self):
        ctx = make_context("line1\nline2\nline3")
        result = step_fill_statistics(ctx)
        assert result.result.line_count == 3

    def test_counts_characters(self):
        ctx = make_context("hello")
        result = step_fill_statistics(ctx)
        assert result.result.char_count == 5

    def test_empty_content(self):
        ctx = make_context("")
        result = step_fill_statistics(ctx)
        assert result.result.line_count == 1
        assert result.result.char_count == 0


class TestStepVerifySections:
    def test_all_sections_found(self):
        content = "Expérience Formation Certifications"
        ctx = make_context(content)
        result = step_verify_sections(ctx)
        assert len(result.result.sections_found) == 3
        assert len(result.result.warnings) == 0

    def test_missing_sections_add_warnings(self):
        ctx = make_context("Expérience")
        result = step_verify_sections(ctx)
        assert "Expérience" in result.result.sections_found
        assert len(result.result.warnings) == 2
        assert any("Formation" in w for w in result.result.warnings)

    def test_does_not_change_success(self):
        ctx = make_context("no sections")
        result = step_verify_sections(ctx)
        assert result.result.success is True


class TestStepVerifyContact:
    def test_all_contact_present(self):
        content = 'email: "test@example.com" phone: "123" linkedin: "user"'
        ctx = make_context(content)
        result = step_verify_contact(ctx)
        assert result.result.success is True
        assert len(result.result.errors) == 0
        assert len(result.result.warnings) == 0

    def test_missing_email_is_critical(self):
        ctx = make_context('phone: "123" linkedin: "user"')
        result = step_verify_contact(ctx)
        assert result.result.success is False
        assert any("email" in e.lower() for e in result.result.errors)

    def test_missing_phone_is_warning(self):
        ctx = make_context('email: "test@example.com" linkedin: "user"')
        result = step_verify_contact(ctx)
        assert result.result.success is True
        assert any("phone" in w.lower() for w in result.result.warnings)

    def test_missing_linkedin_is_warning(self):
        ctx = make_context('email: "test@example.com" phone: "123"')
        result = step_verify_contact(ctx)
        assert result.result.success is True
        assert any("linkedin" in w.lower() for w in result.result.warnings)


class TestStepVerifyEntries:
    def test_counts_entries(self):
        content = "#entry(\n#entry(\n#entry("
        ctx = make_context(content)
        result = step_verify_entries(ctx)
        assert result.result.entry_count == 3

    def test_few_entries_add_warning(self):
        ctx = make_context("#entry(\n#entry(")
        result = step_verify_entries(ctx)
        assert result.result.entry_count == 2
        assert any("peu d'entrées" in w.lower() for w in result.result.warnings)

    def test_enough_entries_no_warning(self):
        content = "#entry(\n" * 5
        ctx = make_context(content)
        result = step_verify_entries(ctx)
        assert result.result.entry_count == 5
        assert len(result.result.warnings) == 0


class TestStepVerifyWhitespace:
    def test_no_trailing_whitespace(self):
        ctx = make_context("line1\nline2\nline3")
        result = step_verify_whitespace(ctx)
        assert len(result.result.warnings) == 0

    def test_trailing_whitespace_adds_warning(self):
        ctx = make_context("line1  \nline2\nline3\t")
        result = step_verify_whitespace(ctx)
        assert any("espaces en fin" in w for w in result.result.warnings)


class TestStepVerifyEncoding:
    def test_no_encoding_errors(self):
        ctx = make_context("Normal content éàù")
        result = step_verify_encoding(ctx)
        assert result.result.success is True
        assert len(result.result.errors) == 0

    def test_encoding_errors_are_critical(self):
        ctx = make_context("Content with ??? errors")
        result = step_verify_encoding(ctx)
        assert result.result.success is False
        assert any("encodage" in e.lower() for e in result.result.errors)


class TestStepVerifyFrenchChars:
    def test_french_chars_present(self):
        ctx = make_context("Expérience à Paris")
        result = step_verify_french_chars(ctx)
        assert len(result.result.warnings) == 0

    def test_no_french_chars_adds_warning(self):
        ctx = make_context("Experience in Paris")
        result = step_verify_french_chars(ctx)
        assert any("accentués" in w for w in result.result.warnings)


class TestCheckSections:
    def test_all_sections_present(self):
        content = "= Expérience\n= Formation\n= Certifications"
        found, missing = check_sections(content)
        assert len(found) == 3
        assert len(missing) == 0

    def test_some_sections_missing(self):
        content = "= Expérience\n= Formation"
        found, missing = check_sections(content)
        assert "Expérience" in found
        assert "Formation" in found
        assert "Certifications" in missing

    def test_no_sections(self):
        content = "Some random content"
        found, missing = check_sections(content)
        assert len(found) == 0
        assert len(missing) == 3


class TestCheckContactInfo:
    def test_all_contact_present(self):
        content = 'email: "test@example.com",\nphone: "(+33)",\nlinkedin: "username",'
        found, missing = check_contact_info(content)
        assert len(found) == 3
        assert len(missing) == 0

    def test_email_missing(self):
        content = 'phone: "(+33)",\nlinkedin: "username",'
        found, missing = check_contact_info(content)
        assert "email" in missing
        assert "phone" in found
        assert "linkedin" in found

    def test_invalid_email(self):
        content = 'email: "not-an-email"'
        found, missing = check_contact_info(content)
        assert "email" in missing


class TestCountEntries:
    def test_count_multiple_entries(self):
        content = '#entry(\n  title: "Job 1",\n)\n\n#entry(\n  title: "Job 2",\n)\n\n#entry(\n  title: "Job 3",\n)'
        count = count_entries(content)
        assert count == 3

    def test_no_entries(self):
        content = "Some content without entries"
        count = count_entries(content)
        assert count == 0


class TestCheckTrailingWhitespace:
    def test_no_trailing_whitespace(self):
        content = "line1\nline2\nline3"
        count = check_trailing_whitespace(content)
        assert count == 0

    def test_with_trailing_whitespace(self):
        content = "line1  \nline2\nline3\t"
        count = check_trailing_whitespace(content)
        assert count == 2


class TestCheckEncodingErrors:
    def test_no_encoding_errors(self):
        content = "Normal content with accents: éàù"
        assert check_encoding_errors(content) is False

    def test_with_encoding_errors(self):
        content = "Content with ??? errors"
        assert check_encoding_errors(content) is True

    def test_few_question_marks(self):
        content = "Is this ok? Yes!"
        assert check_encoding_errors(content) is False


class TestCheckFrenchChars:
    def test_has_french_chars(self):
        content = "Expérience professionnelle à Paris"
        assert check_french_chars(content) is True

    def test_no_french_chars(self):
        content = "Experience in Paris"
        assert check_french_chars(content) is False


class TestVerifyFormat:
    def test_success(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text(
            'email: "test@example.com",\nphone: "+33",\nlinkedin: "user",\n\n= Expérience\n'
            + "#entry(title: Job)\n" * 5
            + "= Etudes\n= Certifications\n= Expertises\n= Langues\n"
        )

        result = verify_format(tmp_path)
        assert result.success is True
        assert len(result.errors) == 0

    def test_failure_missing_email(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text('phone: "+33",\n= Expérience')

        result = verify_format(tmp_path)
        assert result.success is False
        assert any("email" in e.lower() for e in result.errors)

    def test_failure_no_file(self, tmp_path: Path):
        result = verify_format(tmp_path)
        assert result.success is False
        assert any("introuvable" in e.lower() for e in result.errors)

    def test_failure_encoding_error(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text('email: "test@example.com",\nContent with ??? encoding errors')

        result = verify_format(tmp_path)
        assert result.success is False
        assert any("encodage" in e.lower() for e in result.errors)

    def test_pipeline_short_circuits(self, tmp_path: Path):
        cv_file = tmp_path / "src" / "cv.typ"
        cv_file.parent.mkdir(parents=True)
        cv_file.write_text("phone: +33\n??? encoding error")

        result = verify_format(tmp_path)
        assert result.success is False
        assert any("email" in e.lower() for e in result.errors)
        assert not any("encodage" in e.lower() for e in result.errors)


class TestFormatResult:
    def test_default_values(self):
        result = FormatResult(success=True)
        assert result.success is True
        assert result.errors == []
        assert result.warnings == []
        assert result.sections_found == []
        assert result.entry_count == 0
        assert result.line_count == 0
        assert result.char_count == 0
