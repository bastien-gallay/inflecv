"""Tests for company research module."""

from scripts.job_analyze.company_research import (
    CompanyResearchPrompt,
    create_company_research_prompt,
    format_company_section,
)


class TestCreateCompanyResearchPrompt:
    """Test company research prompt generation."""

    def test_create_basic_prompt(self):
        """Should create prompts for a company."""
        result = create_company_research_prompt("TechCorp")

        assert isinstance(result, CompanyResearchPrompt)
        assert result.company == "TechCorp"
        assert len(result.queries) == 3
        assert "TechCorp entreprise taille employés" in result.queries
        assert "TechCorp avis salariés Glassdoor" in result.queries
        assert "TechCorp actualités levée de fonds" in result.queries

    def test_create_prompt_with_sector(self):
        """Should add sector-specific query when provided."""
        result = create_company_research_prompt("Handipulse", sector="EdTech")

        assert len(result.queries) == 4
        assert "Handipulse EdTech innovation" in result.queries

    def test_analysis_prompt_structure(self):
        """Should include structured analysis prompt."""
        result = create_company_research_prompt("TechCorp")

        assert "TechCorp" in result.analysis_prompt
        assert "Secteur d'activité" in result.analysis_prompt
        assert "Taille" in result.analysis_prompt
        assert "Financement" in result.analysis_prompt
        assert "Glassdoor" in result.analysis_prompt


class TestFormatCompanySection:
    """Test company section formatting."""

    def test_format_minimal_section(self):
        """Should format section with minimal info."""
        result = format_company_section(company="TechCorp")

        assert "## Contexte entreprise" in result

    def test_format_section_with_sector(self):
        """Should include sector when provided."""
        result = format_company_section(
            company="TechCorp",
            sector="FinTech",
        )

        assert "**Secteur** : FinTech" in result

    def test_format_section_with_all_fields(self):
        """Should format all fields correctly."""
        result = format_company_section(
            company="Handipulse",
            sector="EdTech / AccessTech",
            size="10-20 employés",
            funding="Seed round 2024",
            glassdoor_rating=4.2,
            highlights=["Mission sociale", "Innovation"],
            concerns=["Early stage", "Petite équipe"],
        )

        assert "**Secteur** : EdTech / AccessTech" in result
        assert "**Taille** : 10-20 employés" in result
        assert "**Financement** : Seed round 2024" in result
        assert "**Note Glassdoor** : 4.2/5" in result
        assert "### Points positifs" in result
        assert "✅ Mission sociale" in result
        assert "### Points d'attention" in result
        assert "⚠️ Early stage" in result

    def test_format_section_without_concerns(self):
        """Should omit concerns section if none provided."""
        result = format_company_section(
            company="TechCorp",
            highlights=["Good culture"],
        )

        assert "### Points positifs" in result
        assert "### Points d'attention" not in result
