from pathlib import Path

import pytest

from scripts.lib import ProjectRoot, ValidatedContent


@pytest.fixture
def sample_cv_content() -> str:
    return """
#import "@preview/neat-cv:0.4.0": cv, entry

#show: cv.with(
  author: (
    firstname: "Test",
    lastname: "User",
    email: "test@example.com",
    phone: "(+33) 06 12 34 56 78",
    linkedin: "testuser",
  ),
)

= Expérience

#entry(
  title: "Senior Developer",
  date: "02/2021 - 10/2025",
  institution: "Company",
)[
  Description
]

#entry(
  title: "Another Job",
  date: "01/2018 - 01/2021",
  institution: "Previous Company",
)[]

#entry(
  title: "First Job",
  date: "06/2015 - 12/2017",
  institution: "Startup",
)[]

= Etudes

#entry(
  title: "Master",
  date: "2020",
  institution: "University",
)[]

#entry(
  title: "Bachelor",
  date: "2018",
  institution: "University",
)[]

= Certifications
= Expertises
= Langues
"""


@pytest.fixture
def validated_cv_content(sample_cv_content: str) -> ValidatedContent:
    return ValidatedContent(sample_cv_content)


@pytest.fixture
def cv_file(tmp_path: Path, sample_cv_content: str) -> Path:
    cv_path = tmp_path / "src" / "cv.typ"
    cv_path.parent.mkdir(parents=True)
    cv_path.write_text(sample_cv_content)
    return cv_path


@pytest.fixture
def valid_project_root(tmp_path: Path, sample_cv_content: str) -> ProjectRoot:
    cv_path = tmp_path / "src" / "cv.typ"
    cv_path.parent.mkdir(parents=True)
    cv_path.write_text(sample_cv_content)
    return ProjectRoot(tmp_path)


@pytest.fixture
def project_with_cv(tmp_path: Path, sample_cv_content: str) -> Path:
    cv_path = tmp_path / "src" / "cv.typ"
    cv_path.parent.mkdir(parents=True)
    cv_path.write_text(sample_cv_content)
    dist_path = tmp_path / "dist"
    dist_path.mkdir()
    return tmp_path


@pytest.fixture
def project_with_pdf(project_with_cv: Path) -> Path:
    pdf_path = project_with_cv / "dist" / "cv.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 dummy content")
    return project_with_cv


@pytest.fixture
def minimal_cv_content() -> str:
    return 'email: "test@example.com"\nphone: "+33"\nlinkedin: "user"\n'


@pytest.fixture
def cv_with_future_dates() -> str:
    return 'date: "02/2021 - 10/2050"\nemail: "test@example.com"'


@pytest.fixture
def cv_with_encoding_errors() -> str:
    return 'email: "test@example.com"\nContent with ??? encoding errors'
