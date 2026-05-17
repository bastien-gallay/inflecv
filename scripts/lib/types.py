from pathlib import Path
from typing import NewType, TypeGuard

RawFileContent = NewType("RawFileContent", str)
ValidatedContent = NewType("ValidatedContent", str)
ProjectRoot = NewType("ProjectRoot", Path)


def is_valid_project_root(path: Path) -> TypeGuard[ProjectRoot]:
    return (path / "src" / "cv.typ").exists()


def is_non_empty_content(content: str) -> TypeGuard[ValidatedContent]:
    return len(content.strip()) > 0
