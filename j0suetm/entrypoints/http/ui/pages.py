import fast_html as html
from starlette.requests import Request
from starlette.responses import HTMLResponse


def render_page(body: list[html.Tag]) -> str:
    return "<!doctype html>" + html.render(
        html.html(
            [html.head(html.script(src="/assets/scripts/htmx.js")), html.body(body)]
        )
    )


async def home(_req: Request) -> HTMLResponse:
    body = [html.button("hello world", hx_get="/test")]
    return HTMLResponse(render_page(body))
