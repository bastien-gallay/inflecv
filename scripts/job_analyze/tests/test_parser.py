"""Tests for job posting parser - TDD approach."""

from scripts.job_analyze.extractors import (
    clean_lines,
    extract_bullet_points,
    extract_company,
    extract_contract_type,
    extract_first_match,
    extract_location,
    extract_salary,
    extract_title,
    is_nice_to_have,
)
from scripts.job_analyze.parser import JobPosting, parse_job_posting
from scripts.job_analyze.patterns import Filters, LocationPatterns
from scripts.job_analyze.types import ContractType, Location


# =============================================================================
# Sample job postings for testing
# =============================================================================

SAMPLE_JOB_SIMPLE = """
Senior Python Developer - TechCorp

Location: Paris, France
Contract: CDI (Full-time)
Salary: 60-80k EUR

About the role:
We are looking for a Senior Python Developer to join our team.

Requirements:
- 5+ years of Python experience (required)
- Experience with Django or FastAPI (required)
- Knowledge of PostgreSQL (required)
- AWS experience (nice to have)
- Docker/Kubernetes (nice to have)

Responsibilities:
- Design and implement backend services
- Mentor junior developers
- Participate in code reviews
"""

SAMPLE_JOB_COMPLEX = """
Chief Technology Officer (CTO) - StartupAI

Paris, France | Remote OK | CDI

Salary: 120-150k EUR + equity

StartupAI is a fast-growing AI startup revolutionizing the healthcare industry.

Mission:
As CTO, you will lead our technical vision and build a world-class engineering team.

Must-have:
- 10+ years software development experience
- 5+ years in leadership roles
- Strong background in Machine Learning / AI
- Experience scaling systems (millions of users)
- Fluent in English

Nice-to-have:
- PhD in Computer Science or related field
- Experience in healthcare/biotech
- Previous startup experience
- Knowledge of regulatory compliance (HIPAA, GDPR)

Tech Stack:
Python, PyTorch, AWS, Kubernetes, PostgreSQL

What we offer:
- Competitive salary + equity
- Flexible working hours
- International team
"""


# =============================================================================
# Tests for Helper Functions
# =============================================================================


class TestGetCleanLines:
    """Tests for clean_lines helper."""

    def test_basic_split(self):
        """Should split text into lines."""
        result = clean_lines("line1\nline2\nline3")
        assert result == ["line1", "line2", "line3"]

    def test_removes_empty_lines(self):
        """Should remove empty lines."""
        result = clean_lines("line1\n\nline2\n\n\nline3")
        assert result == ["line1", "line2", "line3"]

    def test_trims_whitespace(self):
        """Should trim whitespace from lines."""
        result = clean_lines("  line1  \n  line2  ")
        assert result == ["line1", "line2"]

    def test_handles_whitespace_only_lines(self):
        """Should skip whitespace-only lines."""
        result = clean_lines("line1\n   \nline2")
        assert result == ["line1", "line2"]


class TestExtractFirstMatch:
    """Tests for extract_first_match helper."""

    def test_returns_first_match(self):
        """Should return first matching group."""
        patterns = [r"Name:\s*(\w+)", r"Title:\s*(\w+)"]
        result = extract_first_match("Title: Developer", patterns)
        assert result == "Developer"

    def test_returns_none_when_no_match(self):
        """Should return None when nothing matches."""
        patterns = [r"Name:\s*(\w+)"]
        result = extract_first_match("No name here", patterns)
        assert result is None

    def test_tries_patterns_in_order(self):
        """Should try patterns in order."""
        patterns = [r"First:\s*(\w+)", r"Second:\s*(\w+)"]
        result = extract_first_match("First: A Second: B", patterns)
        assert result == "A"


class TestExtractBulletPoints:
    """Tests for extract_bullet_points helper."""

    def test_extracts_dash_bullets(self):
        """Should extract dash bullet points."""
        section = "- Point one here\n- Point two here"
        result = extract_bullet_points(section)
        assert result == ["Point one here", "Point two here"]

    def test_extracts_bullet_char(self):
        """Should extract • bullet points."""
        section = "• First item here\n• Second item here"
        result = extract_bullet_points(section)
        assert result == ["First item here", "Second item here"]

    def test_filters_short_items(self):
        """Should filter items shorter than min_length."""
        section = "- OK this is long enough\n- Short"
        result = extract_bullet_points(section, min_length=10)
        assert result == ["OK this is long enough"]


class TestIsNiceToHaveMarker:
    """Tests for is_nice_to_have helper."""

    def test_detects_nice_to_have(self):
        """Should detect 'nice to have'."""
        assert is_nice_to_have("This is nice to have")
        assert is_nice_to_have("Nice-to-have skill")

    def test_detects_souhaite(self):
        """Should detect 'souhaité' (French)."""
        assert is_nice_to_have("Compétence souhaitée")

    def test_detects_optional(self):
        """Should detect 'optional'."""
        assert is_nice_to_have("This is optional")

    def test_detects_atout(self):
        """Should detect 'atout:' (French)."""
        assert is_nice_to_have("Atout: experience in EdTech")

    def test_returns_false_for_required(self):
        """Should return False for required items."""
        assert not is_nice_to_have("Python (required)")
        assert not is_nice_to_have("This is mandatory")


# =============================================================================
# Tests for Extraction Functions
# =============================================================================


class TestExtractTitle:
    """Tests for extract_title function."""

    def test_extracts_from_dash_separator(self):
        """Should extract title from 'Title - Company' format."""
        lines = ["Software Engineer - TechCorp"]
        assert extract_title(lines) == "Software Engineer"

    def test_extracts_from_at_separator(self):
        """Should extract title from 'Title @ Company' format."""
        lines = ["CTO @ Startup"]
        assert extract_title(lines) == "CTO"

    def test_extracts_from_at_word(self):
        """Should extract title from 'Title at Company' format."""
        lines = ["Developer at BigCo"]
        assert extract_title(lines) == "Developer"

    def test_returns_first_line_as_title(self):
        """Should return first line if no separator found."""
        lines = ["Senior Software Engineer"]
        assert extract_title(lines) == "Senior Software Engineer"

    def test_skips_urls(self):
        """Should return Unknown for URLs."""
        lines = ["https://example.com/jobs"]
        assert extract_title(lines) == "Unknown"

    def test_handles_empty_lines(self):
        """Should return Unknown for empty list."""
        assert extract_title([]) == "Unknown"


class TestExtractCompany:
    """Tests for extract_company function."""

    def test_extracts_from_dash_separator(self):
        """Should extract company from 'Title - Company' format."""
        lines = ["Engineer - TechCorp Inc"]
        assert extract_company(lines, "") == "TechCorp Inc"

    def test_extracts_from_at_separator(self):
        """Should extract company from 'Title @ Company' format."""
        lines = ["CTO @ Startup.io"]
        assert extract_company(lines, "") == "Startup.io"

    def test_extracts_cto_pattern(self):
        """Should extract company from 'CTO COMPANY' pattern."""
        lines = ["CTO HANDIPULSE – Description"]
        text = "CTO HANDIPULSE – Description"
        assert extract_company(lines, text) == "HANDIPULSE"

    def test_extracts_french_pattern(self):
        """Should extract company from 'X est une' pattern."""
        lines = ["Job posting"]
        text = "Handipulse est une deeptech à impact social"
        assert extract_company(lines, text) == "Handipulse"

    def test_returns_unknown_when_not_found(self):
        """Should return Unknown when company not found."""
        lines = ["Just a title"]
        assert extract_company(lines, "No company info") == "Unknown"


class TestExtractLocation:
    """Tests for extract_location function."""

    def test_extracts_explicit_location(self):
        """Should extract from 'Location: X' format."""
        text = "Location: Paris, France"
        assert extract_location(text) == "Paris, France"

    def test_extracts_french_city(self):
        """Should extract French cities."""
        text = "Poste basé à Lyon"
        assert extract_location(text) == "Lyon"

    def test_avoids_nice_to_have_false_positive(self):
        """Should not confuse 'Nice' city with 'nice to have'."""
        text = "This is nice to have but not required"
        assert extract_location(text) is None

    def test_returns_none_when_not_found(self):
        """Should return None when no location found."""
        text = "Remote position anywhere"
        assert extract_location(text) is None


class TestExtractContractType:
    """Tests for extract_contract_type function."""

    def test_extracts_cdi(self):
        """Should extract CDI."""
        assert extract_contract_type("Type: CDI") == "CDI"
        assert extract_contract_type("Poste en CDI") == "CDI"

    def test_normalizes_fulltime_to_cdi(self):
        """Should normalize Full-time to CDI."""
        assert extract_contract_type("(Full-time)") == "CDI"

    def test_extracts_cdd(self):
        """Should extract CDD."""
        assert extract_contract_type("Contrat: CDD") == "CDD"

    def test_extracts_freelance(self):
        """Should extract Freelance."""
        assert extract_contract_type("Mission Freelance") == "Freelance"


class TestExtractSalary:
    """Tests for extract_salary function."""

    def test_extracts_explicit_salary(self):
        """Should extract from 'Salary: X' format."""
        text = "Salary: 50-60k EUR"
        assert extract_salary(text) == "50-60k EUR"

    def test_extracts_range_with_euro(self):
        """Should extract salary ranges with € symbol."""
        text = "50-70k €"
        assert extract_salary(text) == "50-70k €"

    def test_avoids_year_false_positive(self):
        """Should not match year ranges like 2025-2030."""
        text = "Stratégie R&D 2025-2030"
        assert extract_salary(text) is None

    def test_returns_none_when_not_found(self):
        """Should return None when no salary found."""
        text = "Competitive compensation"
        assert extract_salary(text) is None


# =============================================================================
# Tests for Constants
# =============================================================================


class TestConstants:
    """Tests for parser constants."""

    def test_french_cities_list(self):
        """Should contain major French cities."""
        assert "Paris" in LocationPatterns.FRENCH_CITIES
        assert "Lyon" in LocationPatterns.FRENCH_CITIES
        assert "Bordeaux" in LocationPatterns.FRENCH_CITIES

    def test_keyword_false_positives(self):
        """Should contain common false positives."""
        assert "Technologies" in Filters.KEYWORD_FALSE_POSITIVES
        assert "Intelligence" in Filters.KEYWORD_FALSE_POSITIVES


# =============================================================================
# Tests for JobPosting Dataclass
# =============================================================================


class TestJobPostingDataclass:
    """Test JobPosting data structure."""

    def test_create_job_posting(self):
        """Should create a JobPosting with all required fields."""
        job = JobPosting(
            title="Software Engineer",
            company="TechCorp",
            location=Location(city="Paris"),
            contract_type=ContractType.CDI,
        )
        assert job.title == "Software Engineer"
        assert job.company == "TechCorp"
        assert job.location is not None
        assert job.location.city == "Paris"
        assert job.contract_type == ContractType.CDI

    def test_job_posting_optional_fields(self):
        """Should handle optional fields with defaults."""
        job = JobPosting(
            title="Developer",
            company="Corp",
        )
        assert job.location is None
        assert job.salary is None
        assert job.contract_type == ContractType.UNKNOWN
        assert job.must_have == []
        assert job.nice_to_have == []
        assert job.responsibilities == []
        assert job.keywords == []

    def test_job_posting_with_requirements(self):
        """Should store requirements correctly."""
        job = JobPosting(
            title="Developer",
            company="Corp",
            must_have=["Python", "Django"],
            nice_to_have=["Docker"],
        )
        assert "Python" in job.must_have
        assert "Docker" in job.nice_to_have


# =============================================================================
# Tests for parse_job_posting function
# =============================================================================


class TestParseJobPosting:
    """Test job posting parser."""

    def test_parse_simple_job(self):
        """Should parse a simple job posting."""
        job = parse_job_posting(SAMPLE_JOB_SIMPLE)

        assert job.title == "Senior Python Developer"
        assert job.company == "TechCorp"
        assert job.location is not None
        assert job.location.city == "Paris, France"
        assert job.contract_type == ContractType.CDI

    def test_extract_salary(self):
        """Should extract salary information."""
        job = parse_job_posting(SAMPLE_JOB_SIMPLE)
        assert job.salary is not None
        assert str(job.salary) == "60-80k EUR"

    def test_extract_must_have_requirements(self):
        """Should identify must-have requirements."""
        job = parse_job_posting(SAMPLE_JOB_SIMPLE)

        # Should contain key required skills
        must_have_text = " ".join(job.must_have).lower()
        assert "python" in must_have_text
        assert "django" in must_have_text or "fastapi" in must_have_text
        assert "postgresql" in must_have_text

    def test_extract_nice_to_have_requirements(self):
        """Should identify nice-to-have requirements."""
        job = parse_job_posting(SAMPLE_JOB_SIMPLE)

        nice_to_have_text = " ".join(job.nice_to_have).lower()
        assert "aws" in nice_to_have_text or "docker" in nice_to_have_text

    def test_extract_responsibilities(self):
        """Should extract responsibilities."""
        job = parse_job_posting(SAMPLE_JOB_SIMPLE)

        assert len(job.responsibilities) > 0
        resp_text = " ".join(job.responsibilities).lower()
        assert "backend" in resp_text or "mentor" in resp_text

    def test_extract_keywords(self):
        """Should extract ATS keywords."""
        job = parse_job_posting(SAMPLE_JOB_SIMPLE)

        # Should extract technical keywords
        keywords_lower = [k.lower() for k in job.keywords]
        assert "python" in keywords_lower

    def test_parse_complex_job(self):
        """Should parse a complex job posting with multiple sections."""
        job = parse_job_posting(SAMPLE_JOB_COMPLEX)

        assert job.title == "Chief Technology Officer" or "CTO" in job.title
        assert job.company == "StartupAI"
        assert job.location is not None
        assert "Paris" in str(job.location)

    def test_parse_complex_requirements(self):
        """Should correctly categorize complex requirements."""
        job = parse_job_posting(SAMPLE_JOB_COMPLEX)

        # Must-have should include leadership and ML
        must_have_text = " ".join(job.must_have).lower()
        assert "leadership" in must_have_text or "years" in must_have_text

        # Nice-to-have should include PhD, startup
        nice_to_have_text = " ".join(job.nice_to_have).lower()
        assert "phd" in nice_to_have_text or "startup" in nice_to_have_text

    def test_extract_tech_stack_as_keywords(self):
        """Should extract tech stack as keywords."""
        job = parse_job_posting(SAMPLE_JOB_COMPLEX)

        keywords_lower = [k.lower() for k in job.keywords]
        # Should include items from Tech Stack section
        assert any(k in keywords_lower for k in ["python", "pytorch", "aws", "kubernetes"])


# =============================================================================
# Tests for edge cases
# =============================================================================


class TestParserEdgeCases:
    """Test edge cases and error handling."""

    def test_parse_empty_string(self):
        """Should handle empty input gracefully."""
        job = parse_job_posting("")
        assert job.title == "Unknown"
        assert job.company == "Unknown"

    def test_parse_minimal_posting(self):
        """Should handle minimal job posting."""
        minimal = "Software Engineer at Google"
        job = parse_job_posting(minimal)

        assert "Software Engineer" in job.title or "Engineer" in job.title
        assert "Google" in job.company or job.company == "Unknown"

    def test_parse_french_job_posting(self):
        """Should handle French job postings."""
        french_job = """
        Développeur Python Senior - ParisStartup

        Lieu: Paris
        Contrat: CDI

        Exigences:
        - 5 ans d'expérience Python (obligatoire)
        - Connaissance de Django (obligatoire)
        - Anglais courant (souhaité)
        """
        job = parse_job_posting(french_job)

        assert "Python" in job.title or "Développeur" in job.title
        assert len(job.must_have) > 0 or len(job.nice_to_have) > 0

    def test_parse_required_profile_section(self):
        """Should extract requirements from 'Required Profile:' section."""
        linkedin_style = """CTO - TechStartup

Location: Paris
Employment Type: Full-time

Required Profile:

- Solid software engineering background
- Strong knowledge of cloud architectures
- Natural leadership capabilities
"""
        job = parse_job_posting(linkedin_style)

        assert job.title == "CTO"
        assert len(job.must_have) >= 3
        must_have_text = " ".join(job.must_have).lower()
        assert "engineering" in must_have_text or "leadership" in must_have_text
