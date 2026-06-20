import fast_html as html
from pytest_mock import MockerFixture

from j0suetm.domain import fingerprint
from j0suetm.entrypoints.http.ui import document


def test_render_links_fingerprinted_stylesheet(mocker: MockerFixture) -> None:
    css = b"body{}"
    mocker.patch.object(document.fs_in, "get_style", return_value=css)
    name = fingerprint.fingerprint("main.css", css)

    out = document.render([html.p("hi")])

    assert out.startswith("<!doctype html>")
    assert f"/assets/styles/{name}" in out
    assert "/assets/scripts/htmx.js" in out
    assert "<p>hi</p>" in out


def test_render_falls_back_to_plain_name_when_style_missing(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(document.fs_in, "get_style", return_value=None)

    out = document.render([])

    assert "/assets/styles/main.css" in out
