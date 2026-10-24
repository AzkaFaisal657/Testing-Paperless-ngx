from __future__ import annotations

import csv
from pathlib import Path

import pytest

from documents.file_handling import UnsafeFilePathError
from documents.file_handling import validate_path_in_root


def _path_cases() -> list[tuple[str, str, str]]:
    csv_path = Path(__file__).parents[1] / "test_data" / "m2_path_cases.csv"
    with csv_path.open(newline="", encoding="utf-8") as stream:
        return [
            (row["path"], row["expected"])
            for row in csv.DictReader(stream)
        ]


@pytest.mark.documents
@pytest.mark.parametrize(("path", "expected"), _path_cases())
def test_document_path_boundary_cases(
    tmp_path: Path,
    path: str,
    expected: str,
) -> None:
    root = tmp_path / "originals"
    root.mkdir()

    candidate = root / path
    if expected == "inside":
        validate_path_in_root(candidate, root)
    else:
        with pytest.raises(UnsafeFilePathError):
            validate_path_in_root(candidate, root)


@pytest.mark.documents
def test_document_path_equal_to_root_is_allowed(tmp_path: Path) -> None:
    root = tmp_path / "originals"
    root.mkdir()

    validate_path_in_root(root, root)


@pytest.mark.documents
def test_document_path_nested_directory_is_allowed(tmp_path: Path) -> None:
    root = tmp_path / "originals"
    nested = root / "2026" / "October"
    nested.mkdir(parents=True)

    validate_path_in_root(nested / "invoice.pdf", root)
