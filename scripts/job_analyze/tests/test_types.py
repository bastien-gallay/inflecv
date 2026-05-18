"""Tests for domain types module.

CUPID: Tests verify the domain model behavior.
"""

import pytest
from scripts.job_analyze.types import (
    ContractType,
    JobPosting,
    Location,
    Requirement,
    RequirementLevel,
    Salary,
)


class TestRequirementLevel:
    """Tests for RequirementLevel enum."""

    def test_enum_values(self):
        """Should have expected values."""
        assert RequirementLevel.MUST_HAVE.name == "MUST_HAVE"
        assert RequirementLevel.NICE_TO_HAVE.name == "NICE_TO_HAVE"
        assert RequirementLevel.UNKNOWN.name == "UNKNOWN"


class TestContractType:
    """Tests for ContractType enum."""

    def test_from_string_cdi(self):
        """Should parse CDI variants."""
        assert ContractType.from_string("CDI") == ContractType.CDI
        assert ContractType.from_string("Full-time") == ContractType.CDI
        assert ContractType.from_string("Temps plein") == ContractType.CDI

    def test_from_string_cdd(self):
        """Should parse CDD."""
        assert ContractType.from_string("CDD") == ContractType.CDD

    def test_from_string_freelance(self):
        """Should parse Freelance."""
        assert ContractType.from_string("Freelance") == ContractType.FREELANCE

    def test_from_string_stage(self):
        """Should parse Stage/Internship."""
        assert ContractType.from_string("Stage") == ContractType.STAGE
        assert ContractType.from_string("Internship") == ContractType.STAGE

    def test_from_string_unknown(self):
        """Should return Unknown for unrecognized types."""
        assert ContractType.from_string("Contract") == ContractType.UNKNOWN
        assert ContractType.from_string("") == ContractType.UNKNOWN


class TestRequirement:
    """Tests for Requirement dataclass."""

    def test_create_requirement(self):
        """Should create a requirement."""
        req = Requirement("Python 5+ years", RequirementLevel.MUST_HAVE)
        assert req.text == "Python 5+ years"
        assert req.level == RequirementLevel.MUST_HAVE

    def test_is_required(self):
        """Should identify required items."""
        must = Requirement("Python", RequirementLevel.MUST_HAVE)
        nice = Requirement("Docker", RequirementLevel.NICE_TO_HAVE)

        assert must.is_required is True
        assert nice.is_required is False

    def test_is_optional(self):
        """Should identify optional items."""
        must = Requirement("Python", RequirementLevel.MUST_HAVE)
        nice = Requirement("Docker", RequirementLevel.NICE_TO_HAVE)

        assert must.is_optional is False
        assert nice.is_optional is True

    def test_immutable(self):
        """Should be immutable (frozen dataclass)."""
        req = Requirement("Python", RequirementLevel.MUST_HAVE)
        with pytest.raises(AttributeError):
            req.text = "Java"


class TestLocation:
    """Tests for Location dataclass."""

    def test_create_location(self):
        """Should create a location."""
        loc = Location("Paris")
        assert loc.city == "Paris"
        assert loc.country == "France"
        assert loc.remote_ok is False

    def test_location_with_remote(self):
        """Should handle remote flag."""
        loc = Location("Lyon", remote_ok=True)
        assert loc.remote_ok is True

    def test_str_representation(self):
        """Should format as string."""
        loc = Location("Paris")
        assert str(loc) == "Paris, France"

        loc_remote = Location("Lyon", remote_ok=True)
        assert "(Remote OK)" in str(loc_remote)


class TestSalary:
    """Tests for Salary dataclass."""

    def test_create_salary(self):
        """Should create a salary."""
        sal = Salary("50-60k EUR")
        assert sal.raw == "50-60k EUR"
        assert sal.currency == "EUR"

    def test_str_representation(self):
        """Should return raw value as string."""
        sal = Salary("50-60k EUR")
        assert str(sal) == "50-60k EUR"


class TestJobPostingProperties:
    """Tests for JobPosting additional properties."""

    def test_all_requirements(self):
        """Should combine all requirements with levels."""
        job = JobPosting(
            title="Dev",
            company="Corp",
            must_have=["Python", "Django"],
            nice_to_have=["Docker"],
        )
        reqs = job.all_requirements

        assert len(reqs) == 3
        assert reqs[0].level == RequirementLevel.MUST_HAVE
        assert reqs[2].level == RequirementLevel.NICE_TO_HAVE

    def test_keyword_count(self):
        """Should count keywords."""
        job = JobPosting(
            title="Dev",
            company="Corp",
            keywords=["Python", "Django", "AWS"],
        )
        assert job.keyword_count == 3

    def test_has_keyword(self):
        """Should check keyword presence (case-insensitive)."""
        job = JobPosting(
            title="Dev",
            company="Corp",
            keywords=["Python", "Django"],
        )
        assert job.has_keyword("Python") is True
        assert job.has_keyword("python") is True
        assert job.has_keyword("PYTHON") is True
        assert job.has_keyword("Java") is False
