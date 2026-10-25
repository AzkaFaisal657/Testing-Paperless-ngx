from __future__ import annotations

import pytest
from django.test import RequestFactory
from rest_framework.authentication import TokenAuthentication

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
