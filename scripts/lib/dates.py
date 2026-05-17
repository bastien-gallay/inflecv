"""Date parsing utilities with consistent error handling.

CUPID: Predictable - always returns Optional[date], never raises.
CUPID: Unix - single responsibility: parse date strings.
"""

from datetime import date
from typing import Optional


def parse_date(date_str: str) -> Optional[date]:
    """Parse ISO format date string (YYYY-MM-DD).

    Args:
        date_str: Date string or empty/placeholder value

    Returns:
        Parsed date or None if invalid/empty

    Examples:
        >>> parse_date("2025-11-30")
        datetime.date(2025, 11, 30)
        >>> parse_date("-")
        None
        >>> parse_date("invalid")
        None
    """
    if not date_str or date_str.strip() in ("", "-"):
        return None
    try:
        return date.fromisoformat(date_str.strip())
    except ValueError:
        return None
