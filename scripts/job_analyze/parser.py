"""Job posting parser - main orchestrator.

CUPID:
- Composable: Uses extractors as building blocks
- Unix philosophy: Orchestrates, doesn't implement
- Predictable: Single entry point, consistent output
- Idiomatic: Clean Python with type hints
- Domain-based: Returns domain object (JobPosting)
"""

from .extractors import (
    clean_lines,
    extract_company,
    extract_contract_type,
    extract_keywords,
    extract_location,
    extract_must_have,
    extract_nice_to_have,
    extract_responsibilities,
    extract_salary,
    extract_title,
)
from .types import ContractType, JobPosting, Location, Salary

__all__ = [
    "JobPosting",
    "parse_job_posting",
]


# =============================================================================
# Main Parser Function
# =============================================================================


def parse_job_posting(text: str) -> JobPosting:
    """
    Parse a job posting text and extract structured information.

    This is the main entry point for job posting analysis.
    It orchestrates the extraction process using specialized extractors.

    Args:
        text: Raw job posting text (from URL fetch or copy-paste)

    Returns:
        JobPosting with all extracted fields

    Example:
        >>> job = parse_job_posting("Software Engineer - TechCorp\\n...")
        >>> print(job.title)
        "Software Engineer"
        >>> print(job.company)
        "TechCorp"

    The parser handles:
        - French and English job postings
        - Multiple title/company formats (dash, @, "at")
        - Must-have vs nice-to-have requirements
        - ATS keyword extraction
        - Salary and contract type detection
    """
    if not text or not text.strip():
        return JobPosting(title="Unknown", company="Unknown", raw_text=text or "")

    lines = clean_lines(text)

    # Extract raw values
    location_str = extract_location(text)
    contract_str = extract_contract_type(text)
    salary_str = extract_salary(text)

    # Convert to rich types
    location = Location(city=location_str) if location_str else None
    contract_type = ContractType.from_string(contract_str) if contract_str else ContractType.UNKNOWN
    salary = Salary(raw=salary_str) if salary_str else None

    return JobPosting(
        title=extract_title(lines),
        company=extract_company(lines, text),
        location=location,
        contract_type=contract_type,
        salary=salary,
        must_have=extract_must_have(text),
        nice_to_have=extract_nice_to_have(text),
        responsibilities=extract_responsibilities(text),
        keywords=extract_keywords(text),
        raw_text=text,
    )
