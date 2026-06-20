import asyncio
from datetime import datetime
from http import HTTPStatus

import fast_html as html
from pytest_mock import MockerFixture

from j0suetm.entrypoints.http.ui.pages import home

BEGAN_WORKING_AT = 2021


def test_render_shows_identity_and_contacts() -> None:
    out = html.render(home.render())

    assert "Hi, I'm Josué." in out
    assert 'href="mailto:hello@j0suetm.dev"' in out
    assert "github.com/j0suetm" in out
    assert "in/josue-teodoro-moreira" in out


def test_render_external_links_open_new_tab() -> None:
    out = html.render(home.render())

    assert out.count('target="_blank"') == 2
    assert out.count("noopener noreferrer") == 2


def test_render_years_are_relative_to_current_year() -> None:
    expected = datetime.now().year - BEGAN_WORKING_AT

    out = html.render(home.render())

    assert f"{expected}+ years" in out


def test_handle_wraps_view_in_document(mocker: MockerFixture) -> None:
    mocker.patch.object(home.document, "render", return_value="<html>stub</html>")

    resp = asyncio.run(home.handle(None))

    assert resp.status_code == HTTPStatus.OK
    assert resp.media_type == "text/html"
    assert resp.body == b"<html>stub</html>"
