"""Tests for job_fit report generator."""

from scripts.job_fit.report import generate_fit_report
from scripts.job_fit.types import (
    FitLevel,
    FitResult,
    Gap,
    RequirementMatch,
    ScoreBreakdown,
    Strength,
    TalkingPoint,
)


class TestGenerateFitReport:
    """Tests for generate_fit_report function."""

    def test_header_format(self) -> None:
        """Test report header contains title, company, and score."""
        result = FitResult(
            job_title="Senior Developer",
            company="TechCorp",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
        )
        report = generate_fit_report(result)
        assert "# Adéquation : Senior Developer @ TechCorp" in report
        assert "## Score global : 100/100" in report
        assert "⭐⭐⭐⭐⭐" in report

    def test_satisfied_requirements_section(self) -> None:
        """Test satisfied requirements are listed with evidence."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
            must_have_matches=[
                RequirementMatch("Python", FitLevel.SATISFIED, "8 years exp"),
            ],
        )
        report = generate_fit_report(result)
        assert "✅ Exigences obligatoires satisfaites" in report
        assert "Python" in report
        assert "8 years exp" in report

    def test_partial_requirements_section(self) -> None:
        """Test partial requirements are listed with recommendation."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(0.5, 1.0, 1.0, 1.0),
            must_have_matches=[
                RequirementMatch(
                    "Kubernetes",
                    FitLevel.PARTIAL,
                    "Docker experience",
                    "Mention learning in progress",
                ),
            ],
        )
        report = generate_fit_report(result)
        assert "⚠️ Exigences partiellement satisfaites" in report
        assert "Kubernetes" in report
        assert "Docker experience" in report
        assert "Mention learning in progress" in report

    def test_gap_requirements_section(self) -> None:
        """Test gap requirements are listed with strategy."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(0.0, 1.0, 1.0, 1.0),
            must_have_matches=[
                RequirementMatch(
                    "AWS Certification",
                    FitLevel.NOT_SATISFIED,
                    recommendation="Highlight Azure experience instead",
                ),
            ],
        )
        report = generate_fit_report(result)
        assert "❌ Exigences non satisfaites" in report
        assert "AWS Certification" in report
        assert "Highlight Azure experience instead" in report

    def test_strengths_section(self) -> None:
        """Test strengths are listed."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
            strengths=[
                Strength("Leadership", "4 years as CTO"),
                Strength("AI Expertise", "Gen-e2 framework creator"),
            ],
        )
        report = generate_fit_report(result)
        assert "## Points forts à valoriser" in report
        assert "**Leadership**" in report
        assert "4 years as CTO" in report
        assert "**AI Expertise**" in report

    def test_gaps_section(self) -> None:
        """Test gaps are listed with strategies."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(0.5, 0.5, 0.5, 0.5),
            gaps=[
                Gap("Missing Cert", "No AWS cert", "Highlight Azure experience"),
            ],
        )
        report = generate_fit_report(result)
        assert "## Lacunes à adresser" in report
        assert "**Missing Cert**" in report
        assert "Highlight Azure experience" in report

    def test_talking_points_section(self) -> None:
        """Test talking points are listed."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
            talking_points=[
                TalkingPoint("Leadership", "My CTO experience demonstrates..."),
                TalkingPoint("Technical", "I've managed similar projects..."),
            ],
        )
        report = generate_fit_report(result)
        assert "## Talking points pour l'entretien" in report
        assert "My CTO experience demonstrates..." in report
        assert "I've managed similar projects..." in report

    def test_recommendation_section_priority(self) -> None:
        """Test priority recommendation display."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
            justification="Excellent match on all criteria",
        )
        report = generate_fit_report(result)
        assert "## Recommandation finale" in report
        assert "🟢" in report
        assert "Candidature prioritaire" in report
        assert "**Score** : 100/100" in report
        assert "Excellent match on all criteria" in report

    def test_recommendation_section_risky(self) -> None:
        """Test risky recommendation display."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(0.0, 0.0, 0.0, 0.0),
        )
        report = generate_fit_report(result)
        assert "🔴" in report
        assert "Profil peu adapté" in report

    def test_empty_sections_not_included(self) -> None:
        """Test that empty sections are not included."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
            # No must_have_matches, strengths, gaps, or talking_points
        )
        report = generate_fit_report(result)
        # These sections should not appear
        assert "## Points forts à valoriser" not in report
        assert "## Lacunes à adresser" not in report
        assert "## Talking points pour l'entretien" not in report

    def test_nice_to_have_section(self) -> None:
        """Test nice-to-have requirements section."""
        result = FitResult(
            job_title="Dev",
            company="Co",
            score=ScoreBreakdown(1.0, 1.0, 1.0, 1.0),
            nice_to_have_matches=[
                RequirementMatch("Docker", FitLevel.SATISFIED, "5 years"),
            ],
        )
        report = generate_fit_report(result)
        assert "✅ Exigences souhaitées satisfaites" in report
        assert "Docker" in report
