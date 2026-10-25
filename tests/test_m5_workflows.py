from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from documents.data_models import ConsumableDocument
from documents.data_models import DocumentSource
from documents.matching import consumable_document_matches_workflow


def make_trigger(**values):
    defaults = {
        "sources": "",
        "filter_mailrule": None,
        "filter_filename": "",
        "filter_path": "",
    }
    defaults.update(values)
    return SimpleNamespace(**defaults)


@pytest.mark.workflows
@pytest.mark.order(9)
@pytest.mark.parametrize(
    ("filename_pattern", "filename", "expected"),
    [
        ("*.pdf", "invoice.pdf", True),
        ("*.pdf", "invoice.txt", False),
        ("invoice-*.pdf", "invoice-2026.pdf", True),
        ("invoice-*.pdf", "receipt-2026.pdf", False),
        ("", "anything.txt", True),
    ],
)
def test_workflow_filename_filter(
    tmp_path: Path,
    filename_pattern: str,
    filename: str,
    expected: bool,
) -> None:
    file_path = tmp_path / filename
    file_path.write_text("test", encoding="utf-8")
    document = ConsumableDocument(
        source=DocumentSource.ApiUpload,
        original_file=file_path,
    )

    result, reason = consumable_document_matches_workflow(
        document,
        make_trigger(filter_filename=filename_pattern),
    )

    assert result is expected
    assert (reason == "") is expected


@pytest.mark.workflows
@pytest.mark.order(10)
@pytest.mark.parametrize(
    ("source_filter", "source", "expected"),
    [
        ("", DocumentSource.ApiUpload, True),
        ("2", DocumentSource.ApiUpload, True),
        ("1", DocumentSource.ApiUpload, False),
        ("1", DocumentSource.ConsumeFolder, True),
        ("13", DocumentSource.MailFetch, True),
    ],
)
def test_workflow_source_filter(
    tmp_path: Path,
    source_filter: str,
    source: DocumentSource,
    expected: bool,
) -> None:
    file_path = tmp_path / "document.pdf"
    file_path.write_text("test", encoding="utf-8")
    document = ConsumableDocument(source=source, original_file=file_path)

    result, reason = consumable_document_matches_workflow(
        document,
        make_trigger(sources=source_filter),
    )

    assert result is expected
    assert (reason == "") is expected
