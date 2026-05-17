"""Main entry point for verification module.

Usage:
    uv run python -m scripts.verification [--build|--dates|--format]

Options:
    --build   Run only build verification
    --dates   Run only dates verification
    --format  Run only format verification
    (no args) Run all verifications
"""

import argparse
import sys
from pathlib import Path


def find_project_root() -> Path:
    current = Path.cwd()
    while current != current.parent:
        if (current / "src" / "cv.typ").exists():
            return current
        current = current.parent
    return Path.cwd()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify CV quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Run only build verification",
    )
    parser.add_argument(
        "--dates",
        action="store_true",
        help="Run only dates verification",
    )
    parser.add_argument(
        "--format",
        action="store_true",
        help="Run only format verification",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress output, only return exit code",
    )

    args = parser.parse_args()
    project_root = find_project_root()

    # If no specific check requested, run all
    run_all = not (args.build or args.dates or args.format)

    if run_all:
        from .runner import run_all_verifications

        result = run_all_verifications(project_root, verbose=not args.quiet)
        return 0 if result.success else 1

    # Run specific checks
    success = True

    if args.build:
        from .build import print_result, verify_build

        result = verify_build(project_root)
        if not args.quiet:
            print_result(result)
        if not result.success:
            success = False

    if args.dates:
        from .dates import print_result, verify_dates

        result = verify_dates(project_root)
        if not args.quiet:
            print_result(result)
        if not result.success:
            success = False

    if args.format:
        from .format import print_result, verify_format

        result = verify_format(project_root)
        if not args.quiet:
            print_result(result)
        if not result.success:
            success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
