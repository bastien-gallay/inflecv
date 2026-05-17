"""CV verification module.

Provides automated verification tools for the CV:
- Build verification (compilation)
- Date consistency verification
- Format and structure verification
"""

from .build import verify_build
from .dates import verify_dates
from .format import verify_format
from .runner import run_all_verifications

__all__ = ["verify_build", "verify_dates", "verify_format", "run_all_verifications"]
