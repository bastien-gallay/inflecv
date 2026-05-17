"""Markdown metadata table extraction.

CUPID: Domain-based - task metadata is a core domain concept.
CUPID: Composable - returns dict that other modules can consume.
"""

import re
from typing import Dict

# Compiled once for performance
METADATA_FIELD_PATTERN = re.compile(r"\|\s*\*\*([^*]+)\*\*\s*\|\s*([^|]+)\s*\|")


def extract_metadata_table(content: str) -> Dict[str, str]:
    """Extract all metadata fields from markdown table.

    Parses tables like:
        | **Key** | Value |

    Args:
        content: Markdown file content

    Returns:
        Dict mapping field names to stripped values
    """
    return {
        match.group(1).strip(): match.group(2).strip()
        for match in METADATA_FIELD_PATTERN.finditer(content)
        if not match.group(2).strip().startswith("-")
    }


def extract_field(content: str, field: str) -> str:
    """Extract a single metadata field from content.

    Args:
        content: Markdown content
        field: Field name to extract (e.g., "Statut")

    Returns:
        Field value or empty string if not found
    """
    pattern = rf"\|\s*\*\*{re.escape(field)}\*\*\s*\|\s*([^|]+)\s*\|"
    match = re.search(pattern, content)
    return match.group(1).strip() if match else ""
