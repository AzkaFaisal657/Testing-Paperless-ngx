from __future__ import annotations

from unittest.mock import Mock

import pytest

from documents import bulk_edit


@pytest.mark.trash_bulk
@pytest.mark.parametrize(
    ("backup", "expected_calls"),
    [
        ({}, 0),
        ({1: None}, 1),
        ({1: 10, 2: 20}, 2),
        ({0: 0}, 1),
        ({999999: 123}, 1),
    ],
)
def test_restore_archive_serial_numbers_uses_every_backup_entry(
    backup: dict[int, int | None],
    expected_calls: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    update = Mock()
    objects = Mock()
    objects.filter.return_value.update = update
    monkeypatch.setattr(bulk_edit.Document, "objects", objects)

    bulk_edit.restore_archive_serial_numbers(backup)

    assert objects.filter.call_count == expected_calls
    assert update.call_count == expected_calls


@pytest.mark.trash_bulk
def test_restore_archive_serial_numbers_restores_null_asn(monkeypatch) -> None:
    objects = Mock()
    monkeypatch.setattr(bulk_edit.Document, "objects", objects)

    bulk_edit.restore_archive_serial_numbers({7: None})

    objects.filter.assert_called_once_with(pk=7)
    objects.filter.return_value.update.assert_called_once_with(
        archive_serial_number=None,
    )


@pytest.mark.trash_bulk
def test_restore_archive_serial_numbers_restores_numeric_asn(monkeypatch) -> None:
    objects = Mock()
    monkeypatch.setattr(bulk_edit.Document, "objects", objects)

    bulk_edit.restore_archive_serial_numbers({7: 42})

    objects.filter.assert_called_once_with(pk=7)
    objects.filter.return_value.update.assert_called_once_with(
        archive_serial_number=42,
    )
