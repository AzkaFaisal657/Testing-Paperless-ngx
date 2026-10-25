from __future__ import annotations

import csv
from pathlib import Path
from unittest.mock import Mock

import pytest
from django.test import RequestFactory
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

import paperless.auth as paperless_auth
from paperless.auth import PaperlessBasicAuthentication


def _auth_cases() -> list[tuple[str, str | None, str]]:
    csv_path = Path(__file__).parents[1] / "test_data" / "m1_auth_cases.csv"
    with csv_path.open(newline="", encoding="utf-8") as stream:
        return [
            (
                row["case_id"],
                row["authorization"] if row["present"] == "true" else None,
                row["expected"],
            )
            for row in csv.DictReader(stream)
        ]


AUTH_CASES = _auth_cases()


@pytest.mark.auth
@pytest.mark.parametrize(
    ("authorization", "expected"),
    [(authorization, expected) for _, authorization, expected in AUTH_CASES],
    ids=[case_id for case_id, _, _ in AUTH_CASES],
)
def test_basic_authentication_header_cases_from_csv(
    authorization: str | None,
    expected: str,
) -> None:
    request = RequestFactory().get("/")
    if authorization is not None:
        request.META["HTTP_AUTHORIZATION"] = authorization

    assert PaperlessBasicAuthentication().authenticate_header(request) == expected


@pytest.mark.auth
@pytest.mark.parametrize(
    ("authorization", "expected"),
    [
        ("Basic dXNlcjpwYXNz", 'Basic realm="api"'),
        ("basic dXNlcjpwYXNz", 'Basic realm="api"'),
        ("Bearer token", TokenAuthentication.keyword),
        ("", TokenAuthentication.keyword),
        (None, TokenAuthentication.keyword),
    ],
)
def test_basic_authentication_header_boundary(
    authorization: str | None,
    expected: str,
) -> None:
    request = RequestFactory().get("/")
    if authorization is not None:
        request.META["HTTP_AUTHORIZATION"] = authorization

    result = PaperlessBasicAuthentication().authenticate_header(request)

    assert result == expected


@pytest.mark.auth
def test_basic_authentication_rejects_user_when_mfa_is_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = RequestFactory().get(
        "/",
        HTTP_AUTHORIZATION="Basic dXNlcjpwYXNz",
    )
    user = Mock()
    adapter = Mock()
    adapter.is_mfa_enabled.return_value = True
    monkeypatch.setattr(
        PaperlessBasicAuthentication,
        "authenticate_credentials",
        lambda self, request, userid, password: (user, None),
    )
    monkeypatch.setattr(paperless_auth, "get_mfa_adapter", lambda: adapter)

    with pytest.raises(AuthenticationFailed, match="MFA required"):
        PaperlessBasicAuthentication().authenticate(request)


@pytest.mark.auth
def test_basic_authentication_returns_user_when_mfa_is_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = RequestFactory().get(
        "/",
        HTTP_AUTHORIZATION="Basic dXNlcjpwYXNz",
    )
    user = Mock()
    adapter = Mock()
    adapter.is_mfa_enabled.return_value = False
    monkeypatch.setattr(
        PaperlessBasicAuthentication,
        "authenticate_credentials",
        lambda self, request, userid, password: (user, None),
    )
    monkeypatch.setattr(paperless_auth, "get_mfa_adapter", lambda: adapter)

    assert PaperlessBasicAuthentication().authenticate(request) == (user, None)
