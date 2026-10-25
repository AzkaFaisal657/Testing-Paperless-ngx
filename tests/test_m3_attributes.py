from __future__ import annotations

import pytest

from documents import matching
from documents.models import MatchingModel
from documents.models import Tag


@pytest.mark.attributes
@pytest.mark.order(4)
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  invoice   2026  ", [r"invoice", r"2026"]),
        ('invoice "tax document"', [r"invoice", r"tax\s+document"]),
        ("", []),
        ("one two three", [r"one", r"two", r"three"]),
        ('"two words" final', [r"two\s+words", r"final"]),
    ],
)
def test_attribute_match_text_is_split_into_keywords(
    text: str,
    expected: list[str],
) -> None:
    tag = Tag(match=text)

    assert matching._split_match(tag) == expected


@pytest.mark.attributes
@pytest.mark.order(5)
@pytest.mark.parametrize(
    ("algorithm", "pattern", "content", "expected"),
    [
        (MatchingModel.MATCH_ANY, "invoice", "March invoice", True),
        (MatchingModel.MATCH_ANY, "invoice", "March receipt", False),
        (MatchingModel.MATCH_ALL, "march invoice", "March invoice", True),
        (MatchingModel.MATCH_ALL, "march invoice", "March receipt", False),
        (MatchingModel.MATCH_LITERAL, "tax document", "Tax document", True),
        (MatchingModel.MATCH_REGEX, r"INV-\d+", "INV-123", True),
        (MatchingModel.MATCH_REGEX, r"INV-\d+", "receipt", False),
        (MatchingModel.MATCH_NONE, "invoice", "March invoice", False),
    ],
)
def test_attribute_matching_algorithms(
    algorithm: int,
    pattern: str,
    content: str,
    expected: bool,
) -> None:
    tag = Tag(
        match=pattern,
        matching_algorithm=algorithm,
        is_insensitive=True,
    )
    from documents.models import Document

    document = Document(content=content)

    assert matching.matches(tag, document) is expected
