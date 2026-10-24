from __future__ import annotations

from unittest.mock import Mock

import pytest
from django.test import RequestFactory
from django.test import override_settings
from rest_framework.authentication import TokenAuthentication

from paperless.auth import AngularApiAuthenticationOverride
from paperless.auth import PaperlessBasicAuthentication


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
@pytest.mark.parametrize(
    ("debug", "referer", "staff_user", "expected_authenticated"),
    [
        (True, "http://localhost:4200/", Mock(is_staff=True), True),
        (True, "http://localhost:4200/app", Mock(is_staff=True), True),
        (True, "https://localhost:4200/", Mock(is_staff=True), False),
        (False, "http://localhost:4200/", Mock(is_staff=True), False),
        (True, "http://localhost:4201/", Mock(is_staff=True), False),
        (True, "http://localhost:4200/", None, False),
    ],
)
def test_angular_dev_server_authentication_boundaries(
    debug: bool,
    referer: str,
    staff_user: Mock | None,
    expected_authenticated: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = RequestFactory().get("/", HTTP_REFERER=referer)
    user_manager = Mock()
    user_manager.filter.return_value.first.return_value = staff_user
    monkeypatch.setattr("paperless.auth.User.objects", user_manager)

    with override_settings(DEBUG=debug):
        result = AngularApiAuthenticationOverride().authenticate(request)

    if staff_user is None:
        assert result == (None, None)
    elif expected_authenticated:
        assert result == (staff_user, None)
    else:
        assert result is None
