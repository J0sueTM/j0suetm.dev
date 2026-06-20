import fast_html as html

from j0suetm.domain import fingerprint
from j0suetm.services.inbound import fs_in


def _style_href(fname: str) -> str:
    content = fs_in.get_style(fname)
    name = fingerprint.fingerprint(fname, content) if content else fname
    return f"/assets/styles/{name}"


def render(body: list[html.Tag]) -> str:
    return "<!doctype html>" + html.render(
        html.html(
            [
                html.head(
                    [
                        html.meta(charset="utf-8"),
                        html.meta(
                            name="viewport",
                            content="width=device-width, initial-scale=1",
                        ),
                        html.script(src="/assets/scripts/htmx.js"),
                        html.link(rel="stylesheet", href=_style_href("main.css")),
                    ]
                ),
                html.body(body),
            ]
        )
    )
