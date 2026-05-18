"""Pure extraction functions for job posting parsing.

CUPID:
- Composable: Each function does one extraction, can be combined
- Unix philosophy: Each function has a single responsibility
- Predictable: Pure functions with consistent return types
- Idiomatic: Type hints, docstrings, Pythonic patterns
"""

import re
from collections.abc import Callable, Iterable
from typing import TypeVar

from .patterns import (
    ContractPatterns,
    Filters,
    LocationPatterns,
    RequirementMarkers,
    SectionHeaders,
    SectionTerminators,
    TechKeywords,
    TitlePatterns,
)

T = TypeVar("T")


# =============================================================================
# Generic Extractors (Composable building blocks)
# =============================================================================


def extract_first_match(
    text: str,
    patterns: Iterable[str],
    group: int = 1,
    flags: int = re.IGNORECASE | re.DOTALL,
) -> str | None:
    """Extract first matching group from patterns.

    CUPID: Composable - generic extractor that can be reused.
    """
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            return match.group(group).strip()
    return None


def extract_all_matches(
    text: str,
    pattern: str,
    flags: int = re.IGNORECASE,
) -> list[str]:
    """Extract all matches for a pattern.

    CUPID: Composable - returns list for further processing.
    """
    matches = re.findall(pattern, text, flags)
    return [m if isinstance(m, str) else m[0] for m in matches]


def extract_section(
    text: str,
    headers: Iterable[str],
    terminators: str,
) -> str | None:
    """Extract a section by its header pattern.

    CUPID: Composable - generic section extractor.
    """
    header_pattern = "|".join(headers)
    pattern = f"(?:{header_pattern}).*?(?={terminators})"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(0) if match else None


def extract_bullet_points(
    section: str,
    min_length: int = 10,
) -> list[str]:
    """Extract bullet points from a section.

    CUPID: Composable - works with any section text.
    """
    bullets = re.findall(r"[-•*]\s*(.+?)(?=\n[-•*]|\n\n|\Z)", section, re.DOTALL)
    results = []
    for bullet in bullets:
        cleaned = bullet.strip().replace("\n", " ")
        if cleaned and len(cleaned) >= min_length:
            results.append(cleaned)
    return results


def filter_items(
    items: Iterable[T],
    predicate: Callable[[T], bool],
) -> list[T]:
    """Filter items by predicate.

    CUPID: Composable - generic filter.
    """
    return [item for item in items if predicate(item)]


def clean_lines(text: str) -> list[str]:
    """Split text into non-empty trimmed lines.

    CUPID: Unix philosophy - does one thing.
    """
    lines = text.strip().split("\n")
    return [line.strip() for line in lines if line.strip()]


# =============================================================================
# Marker Detection (Predicates)
# =============================================================================


def is_nice_to_have(text: str) -> bool:
    """Check if text contains nice-to-have markers.

    CUPID: Predictable - pure predicate function.
    """
    pattern = "|".join(RequirementMarkers.NICE_TO_HAVE)
    return bool(re.search(pattern, text, re.IGNORECASE))


def is_required(text: str) -> bool:
    """Check if text contains required markers.

    CUPID: Predictable - pure predicate function.
    """
    pattern = "|".join(RequirementMarkers.REQUIRED)
    return bool(re.search(pattern, text, re.IGNORECASE))


def is_url(text: str) -> bool:
    """Check if text looks like a URL.

    CUPID: Predictable - pure predicate function.
    """
    return text.startswith(("http", "www"))


def is_year_range(text: str) -> bool:
    """Check if text looks like a year range (e.g., 2025-2030).

    CUPID: Predictable - pure predicate function.
    """
    return bool(re.match(r"^20\d{2}", text))


# =============================================================================
# Domain-Specific Extractors
# =============================================================================


def extract_title(lines: list[str]) -> str:
    """Extract job title from first line.

    CUPID: Domain-based - specific to job posting structure.
    """
    if not lines:
        return "Unknown"

    first_line = lines[0]

    # Check for separators
    for separator in TitlePatterns.SEPARATORS:
        if separator.lower() in first_line.lower():
            if separator == " at ":
                idx = first_line.lower().index(separator)
                return first_line[:idx].strip()
            if separator in first_line:
                return first_line.split(separator)[0].strip()

    # Use first line if it looks like a title
    if len(first_line) < 100 and not is_url(first_line):
        return first_line

    return "Unknown"


def extract_company(lines: list[str], text: str) -> str:
    """Extract company name from posting.

    CUPID: Domain-based - tries multiple strategies.
    """
    if lines:
        # Try separator patterns
        company = _extract_company_from_separators(lines[0])
        if company:
            return company

        # Try executive title pattern (e.g., "CTO HANDIPULSE")
        company = _extract_company_from_executive_title(lines[0])
        if company:
            return company

    # Try text patterns
    company = _extract_company_from_text(text)
    if company:
        return company

    return "Unknown"


def _extract_company_from_separators(first_line: str) -> str | None:
    """Extract company using separator patterns."""
    for separator in TitlePatterns.SEPARATORS:
        if separator == " at ":
            if separator in first_line.lower():
                idx = first_line.lower().index(separator)
                return first_line[idx + len(separator) :].strip()
        elif separator in first_line:
            parts = first_line.split(separator)
            if len(parts) >= 2:
                return parts[1].strip()
    return None


def _extract_company_from_executive_title(first_line: str) -> str | None:
    """Extract company from executive title pattern."""
    titles = "|".join(TitlePatterns.EXECUTIVE_TITLES)
    match = re.search(rf"(?:{titles})\s+([A-Z][A-Z0-9]+)", first_line)
    return match.group(1).strip() if match else None


def _extract_company_from_text(text: str) -> str | None:
    """Extract company from text patterns."""
    patterns = [
        r"(?:chez|at|@)\s+([A-Z][A-Za-z0-9\s]+)",
        r"(?:Company|Entreprise|Société)\s*:\s*([^\n]+)",
        r"([A-Z][A-Za-z0-9]+)\s+est\s+un",  # French pattern
    ]
    return extract_first_match(text, patterns)


def extract_location(text: str) -> str | None:
    """Extract location from posting.

    CUPID: Domain-based - handles French cities and patterns.
    """
    # Try explicit patterns first
    patterns = [
        r"(?:Location|Lieu|Localisation)\s*:\s*([^\n|]+)",
    ]
    location = extract_first_match(text, patterns)
    if location:
        return location

    # Try city patterns
    cities_pattern = "|".join(LocationPatterns.FRENCH_CITIES)
    city_patterns = [
        rf"(?:basé|based|situé|located)\s+(?:à|in|at)\s+({cities_pattern})",
        rf"({cities_pattern}),?\s*France",
    ]

    for pattern in city_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            # Avoid "nice to have" false positive
            if location.lower() == "nice" and "nice to have" in text.lower():
                continue
            return location

    return None


def extract_contract_type(text: str) -> str | None:
    """Extract contract type from posting.

    CUPID: Domain-based - normalizes contract types.
    """
    types_pattern = "|".join(ContractPatterns.TYPES)
    patterns = [
        rf"(?:Contract|Contrat|Type)\s*:\s*({types_pattern})",
        rf"\b({types_pattern})\b",
        rf"\(({types_pattern})\)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            contract = match.group(1).strip()
            # Normalize
            if contract.lower() in ("full-time", "temps plein"):
                return "CDI"
            return contract.upper() if len(contract) <= 4 else contract

    return None


def extract_salary(text: str) -> str | None:
    """Extract salary from posting.

    CUPID: Domain-based - handles currency formats.
    """
    patterns = [
        r"(?:Salary|Salaire|Rémunération)\s*:\s*([^\n]+)",
        r"(\d{2,3}[-–]\d{2,3}\s*k?\s*(?:EUR|€|K€|K))",
        r"(\d{2,3}\s*(?:à|to)\s*\d{2,3}\s*k?\s*(?:EUR|€|K€|K))",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            salary = match.group(1).strip()
            # Avoid year ranges
            if is_year_range(salary):
                continue
            return salary

    return None


def extract_must_have(text: str) -> list[str]:
    """Extract must-have requirements.

    CUPID: Composable - uses generic extractors.
    """
    must_have = []

    # Extract from requirements section
    section = extract_section(
        text,
        SectionHeaders.REQUIREMENTS,
        SectionTerminators.REQUIREMENTS,
    )
    if section:
        bullets = extract_bullet_points(section)
        for bullet in bullets:
            if not is_nice_to_have(bullet):
                # Clean (required) marker if present
                if is_required(bullet):
                    bullet = re.sub(r"\s*\(.*?\)\s*", " ", bullet).strip()
                must_have.append(bullet)

    # Also find inline (required) markers
    inline = re.findall(r"[-•*]\s*(.+?)\s*\(required\)", text, re.IGNORECASE)
    for req in inline:
        if req.strip() not in must_have:
            must_have.append(req.strip())

    return must_have


def extract_nice_to_have(text: str) -> list[str]:
    """Extract nice-to-have requirements.

    CUPID: Composable - uses generic extractors.
    """
    nice_to_have = []

    # Extract from nice-to-have section
    section = extract_section(
        text,
        SectionHeaders.NICE_TO_HAVE,
        SectionTerminators.GENERIC,
    )
    if section:
        bullets = re.findall(r"[-•*]\s*(.+?)(?=\n|$)", section)
        nice_to_have.extend([b.strip() for b in bullets])

    # Find inline markers
    inline = re.findall(
        r"[-•*]\s*(.+?)\s*\((?:nice.to.have|souhaité|optional)\)",
        text,
        re.IGNORECASE,
    )
    nice_to_have.extend([n.strip() for n in inline])

    # French "Atout:" pattern
    atout_match = re.search(r"Atout\s*:\s*(.+?)(?=\n[-•*]|\n\n|\Z)", text, re.IGNORECASE)
    if atout_match:
        atout = atout_match.group(1).strip()
        if atout and atout not in nice_to_have:
            nice_to_have.append(atout)

    return nice_to_have


def extract_responsibilities(text: str) -> list[str]:
    """Extract job responsibilities.

    CUPID: Composable - uses generic extractors.
    """
    section = extract_section(
        text,
        SectionHeaders.RESPONSIBILITIES,
        SectionTerminators.RESPONSIBILITIES,
    )
    if section:
        return extract_bullet_points(section)
    return []


def extract_keywords(text: str) -> list[str]:
    """Extract ATS keywords from posting.

    CUPID: Composable - combines multiple keyword sources.
    """
    keywords: set[str] = set()

    # Use TechKeywords.all_groups() for clean iteration
    for group in TechKeywords.all_groups():
        # Escape special regex characters
        escaped = [re.escape(kw).replace(r"\ ", r"\s*") for kw in group]
        pattern = r"\b(" + "|".join(escaped) + r")\b"
        matches = extract_all_matches(text, pattern)
        keywords.update(matches)

    # Extract from Tech Stack section
    stack_section = extract_section(
        text,
        ("Tech Stack", "Stack Technique"),
        SectionTerminators.GENERIC,
    )
    if stack_section:
        techs = re.findall(r"\b([A-Z][A-Za-z0-9+#.]+)\b", stack_section)
        keywords.update(techs)

    # Filter false positives
    keywords = keywords - Filters.KEYWORD_FALSE_POSITIVES

    return sorted(keywords, key=str.lower)
