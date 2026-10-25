from __future__ import annotations

from unittest.mock import Mock

import pytest

from documents.filters import ObjectFilter


@pytest.mark.search_views
@pytest.mark.order(6)
@pytest.mark.parametrize(
    ("value", "expected_calls"),
    [
        ("", 0),
        (None, 0),
        ("not-a-number", 0),
        ("12", 1),
        ("12,13", 2),
    ],
)
def test_object_filter_handles_search_filter_values(
    value: str | None,
    expected_calls: int,
) -> None:
    queryset = Mock()
    queryset.filter.return_value = queryset
    queryset.exclude.return_value = queryset
    object_filter = ObjectFilter(field_name="tags")

    result = object_filter.filter(queryset, value)

    assert result is queryset
    assert queryset.filter.call_count == expected_calls


@pytest.mark.search_views
@pytest.mark.order(7)
def test_object_filter_can_filter_for_a_list_of_ids() -> None:
    queryset = Mock()
    queryset.filter.return_value = queryset
    object_filter = ObjectFilter(field_name="tags", in_list=True)

    object_filter.filter(queryset, "4,5")

    queryset.filter.assert_called_once_with(tags__id__in=[4, 5])
    queryset.distinct.assert_called_once_with()


@pytest.mark.search_views
@pytest.mark.order(8)
def test_object_filter_can_exclude_ids() -> None:
    queryset = Mock()
    queryset.exclude.return_value = queryset
    object_filter = ObjectFilter(field_name="tags", exclude=True)

    object_filter.filter(queryset, "4,5")

    assert queryset.exclude.call_count == 2
    queryset.exclude.assert_any_call(tags__id=4)
    queryset.exclude.assert_any_call(tags__id=5)
