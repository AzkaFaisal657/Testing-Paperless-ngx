from __future__ import annotations

import csv
from pathlib import Path
from types import SimpleNamespace

import pytest

from documents.data_models import DocumentSource
from documents.matching import consumable_document_matches_workflow
from documents.matching import matches
from documents.models import Document
from documents.models import MatchingModel
from documents.models import WorkflowTrigger


def _workflow_matching_cases() -> list[tuple[str, str, str, str, bool, bool]]:
    csv_path = (
        Path(__file__).parents[1]
        / "test_data"
        / "m5_workflow_matching_cases.csv"
    )
    with csv_path.open(newline="", encoding="utf-8") as stream:
        return [
            (
                row["case_id"],
                row["algorithm"],
                row["pattern"],
                row["content"],
                row["is_insensitive"].lower() == "true",
                row["expected"].lower() == "true",
            )
            for row in csv.DictReader(stream)
        ]


def _workflow_filter_cases() -> list[dict[str, str]]:
    csv_path = (
        Path(__file__).parents[1]
        / "test_data"
        / "m5_workflow_filter_cases.csv"
    )
    with csv_path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


WORKFLOW_MATCHING_CASES = _workflow_matching_cases()
WORKFLOW_FILTER_CASES = _workflow_filter_cases()


@pytest.mark.workflows
@pytest.mark.parametrize(
    ("algorithm", "pattern", "content", "is_insensitive", "expected"),
    [case[1:] for case in WORKFLOW_MATCHING_CASES],
    ids=[case[0] for case in WORKFLOW_MATCHING_CASES],
)
def test_workflow_content_matching(
    algorithm: str,
    pattern: str,
    content: str,
    is_insensitive: bool,
    expected: bool,
) -> None:
    trigger = WorkflowTrigger(
        match=pattern,
        matching_algorithm=getattr(MatchingModel, f"MATCH_{algorithm.upper()}"),
        is_insensitive=is_insensitive,
    )

    assert matches(trigger, Document(content=content)) is expected


@pytest.mark.workflows
@pytest.mark.parametrize(
    "case",
    WORKFLOW_FILTER_CASES,
    ids=[case["case_id"] for case in WORKFLOW_FILTER_CASES],
)
def test_consumption_workflow_source_filename_and_path_filters(
    case: dict[str, str],
) -> None:
    document_source = getattr(DocumentSource, case["document_source"])
    trigger_sources = (
        [str(int(getattr(DocumentSource, case["trigger_source"])))]
        if case["trigger_source"]
        else []
    )
    document = SimpleNamespace(
        source=document_source,
        mailrule_id=None,
        original_file=(
            Path(case["filename"]) if case["filename"] else Path("invoice.pdf")
        ),
        original_path=case["original_path"] or None,
    )
    trigger = SimpleNamespace(
        sources=trigger_sources,
        filter_mailrule=None,
        filter_filename=case["filename_filter"] or None,
        filter_path=case["path_filter"] or None,
    )

    matched, _ = consumable_document_matches_workflow(document, trigger)

    assert matched is (case["expected"].lower() == "true")
