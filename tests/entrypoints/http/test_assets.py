from http import HTTPStatus

from starlette.testclient import TestClient
from pytest_mock import MockerFixture

from j0suetm.domain import fingerprint
from j0suetm.entrypoints.http import assets
from j0suetm.entrypoints.cli import start_app


def _client() -> TestClient:
    return TestClient(start_app())


# ---- htmx script: filesystem hit vs CDN fallback ----


def test_htmx_served_from_filesystem_without_hitting_cdn(mocker: MockerFixture) -> None:
    mocker.patch.object(assets.fs_in, "get_script", return_value=b"local-htmx")
    cdn = mocker.patch.object(assets.http_in, "get_htmx_script")
    save = mocker.patch.object(assets.fs_out, "save_script")

    resp = _client().get("/assets/scripts/htmx.js")

    assert resp.status_code == HTTPStatus.OK
    assert resp.content == b"local-htmx"
    assert resp.headers["content-type"].startswith("text/javascript")
    cdn.assert_not_called()
    save.assert_not_called()


def test_htmx_falls_back_to_cdn_and_caches(mocker: MockerFixture) -> None:
    mocker.patch.object(assets.fs_in, "get_script", return_value=None)
    mocker.patch.object(assets.http_in, "get_htmx_script", return_value=b"cdn-htmx")
    save = mocker.patch.object(assets.fs_out, "save_script")

    resp = _client().get("/assets/scripts/htmx.js")

    assert resp.content == b"cdn-htmx"
    save.assert_called_once()
    fname, content = save.call_args.args
    assert "htmx" in fname
    assert content == b"cdn-htmx"


# ---- styles: content-hash gate ----


def test_style_served_when_hash_matches_content(mocker: MockerFixture) -> None:
    css = b"body{color:red}"
    mocker.patch.object(assets.fs_in, "get_style", return_value=css)
    name = fingerprint.fingerprint("main.css", css)

    resp = _client().get(f"/assets/styles/{name}")

    assert resp.status_code == HTTPStatus.OK
    assert resp.content == css
    assert resp.headers["content-type"].startswith("text/css")
    assert resp.headers["cache-control"] == assets.IMMUTABLE_CACHE


def test_style_404_when_hash_does_not_match(mocker: MockerFixture) -> None:
    mocker.patch.object(assets.fs_in, "get_style", return_value=b"body{}")

    resp = _client().get("/assets/styles/main.000000000000.css")

    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_style_404_when_file_absent(mocker: MockerFixture) -> None:
    mocker.patch.object(assets.fs_in, "get_style", return_value=None)

    resp = _client().get("/assets/styles/main.000000000000.css")

    assert resp.status_code == HTTPStatus.NOT_FOUND


def test_style_404_for_unhashed_name(mocker: MockerFixture) -> None:
    get_style = mocker.patch.object(assets.fs_in, "get_style")

    resp = _client().get("/assets/styles/main.css")

    assert resp.status_code == HTTPStatus.NOT_FOUND
    get_style.assert_not_called()
