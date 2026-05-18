"""Tests for job posting report generator."""

from scripts.job_analyze.report import generate_report
from scripts.job_analyze.types import ContractType, JobPosting, Location, Salary


class TestGenerateReport:
    """Test report generation."""

    def test_generate_basic_report(self):
        """Should generate a report with basic info."""
        job = JobPosting(
            title="Software Engineer",
            company="TechCorp",
            location=Location(city="Paris"),
            contract_type=ContractType.CDI,
        )
        report = generate_report(job)

        assert "# Analyse : Software Engineer @ TechCorp" in report
        assert "**Poste**: Software Engineer" in report
        assert "**Entreprise**: TechCorp" in report
        assert "**Localisation**: Paris, France" in report
        assert "**Type de contrat**: CDI" in report

    def test_generate_report_with_requirements(self):
        """Should include requirements in report."""
        job = JobPosting(
            title="Developer",
            company="Corp",
            must_have=["Python 5+ years", "Django experience"],
            nice_to_have=["Docker knowledge"],
        )
        report = generate_report(job)

        assert "## Exigences" in report
        assert "### Obligatoires (2)" in report
        assert "Python 5+ years" in report
        assert "### Souhaitées (1)" in report
        assert "Docker knowledge" in report

    def test_generate_report_with_responsibilities(self):
        """Should include responsibilities in report."""
        job = JobPosting(
            title="Lead Dev",
            company="Corp",
            responsibilities=["Lead team", "Code review", "Architecture"],
        )
        report = generate_report(job)

        assert "## Responsabilités principales" in report
        assert "1. Lead team" in report
        assert "2. Code review" in report

    def test_generate_report_with_keywords(self):
        """Should include ATS keywords in report."""
        job = JobPosting(
            title="Developer",
            company="Corp",
            keywords=["Python", "Django", "PostgreSQL"],
        )
        report = generate_report(job)

        assert "## Mots-clés ATS" in report
        assert "`Python`" in report
        assert "`Django`" in report

    def test_generate_report_with_salary(self):
        """Should include salary when provided."""
        job = JobPosting(
            title="Developer",
            company="Corp",
            salary=Salary(raw="50-60k EUR"),
        )
        report = generate_report(job)

        assert "**Salaire**: 50-60k EUR" in report

    def test_generate_report_omits_empty_sections(self):
        """Should not include empty sections."""
        job = JobPosting(
            title="Developer",
            company="Corp",
        )
        report = generate_report(job)

        # Should not have empty requirements section content
        assert "### Obligatoires (0)" not in report
        assert "### Souhaitées (0)" not in report
