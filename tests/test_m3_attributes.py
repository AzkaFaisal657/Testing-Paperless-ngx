from __future__ import annotations

import csv
from pathlib import Path

import pytest
from rest_framework.exceptions import ValidationError

from documents.serialisers import CustomFieldSerializer


def _custom_field_type_cases() -> list[tuple[str, str]]:
    csv_path = Path(__file__).parents[1] / "test_data" / "m3_custom_field_types.csv"
    with csv_path.open(newline="", encoding="utf-8") as stream:
        return [
            (row["case_id"], row["data_type"])
            for row in csv.DictReader(stream)
        ]


CUSTOM_FIELD_TYPE_CASES = _custom_field_type_cases()


@pytest.mark.attributes
@pytest.mark.parametrize(
    "data_type",
    [data_type for _, data_type in CUSTOM_FIELD_TYPE_CASES],
    ids=[case_id for case_id, _ in CUSTOM_FIELD_TYPE_CASES],
)
def test_custom_field_serializer_accepts_supported_data_type(
    data_type: str,
) -> None:
    field = CustomFieldSerializer().fields["data_type"]

    assert field.run_validation(data_type) == data_type


@pytest.mark.attributes
def test_custom_field_serializer_rejects_unsupported_data_type() -> None:
    field = CustomFieldSerializer().fields["data_type"]

    with pytest.raises(ValidationError):
        field.run_validation("unsupported")


@pytest.mark.attributes
def test_custom_field_serializer_requires_a_name() -> None:
    field = CustomFieldSerializer().fields["name"]

    with pytest.raises(ValidationError):
        field.run_validation("")
