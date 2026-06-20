import httpx
import pytest
import respx

from j0suetm.services.inbound import http_in

HTMX_URL = "https://cdn.jsdelivr.net/npm/htmx.org@2.0.10/dist/htmx.min.js"


@respx.mock
def test_get_htmx_script_returns_cdn_body() -> None:
    route = respx.get(HTMX_URL).mock(
        return_value=httpx.Response(200, content=b"htmx-source")
    )

    assert http_in.get_htmx_script() == b"htmx-source"
    assert route.called


@respx.mock
def test_get_htmx_script_propagates_http_error() -> None:
    respx.get(HTMX_URL).mock(return_value=httpx.Response(500))

    with pytest.raises(httpx.HTTPStatusError):
        http_in.get_htmx_script()
