"""Shared utilities for CV project scripts.

This module provides common functionality following CUPID principles:
- Composable: Small functions that can be combined
- Unix: Single responsibility per function
- Predictable: Consistent error handling via Result pattern
- Idiomatic: Python conventions and type hints
- Domain-based: Organized by business domain
"""

from scripts.lib.context import Context, HasSuccess
from scripts.lib.dates import parse_date
from scripts.lib.metadata import extract_field, extract_metadata_table
from scripts.lib.result import Result
from scripts.lib.types import (
    ProjectRoot,
    RawFileContent,
    ValidatedContent,
    is_non_empty_content,
    is_valid_project_root,
)

__all__ = [
    # Context and Result
    "Context",
    "HasSuccess",
    "Result",
    # Types
    "ProjectRoot",
    "RawFileContent",
    "ValidatedContent",
    "is_non_empty_content",
    "is_valid_project_root",
    # Dates
    "parse_date",
    # Metadata
    "extract_field",
    "extract_metadata_table",
]
