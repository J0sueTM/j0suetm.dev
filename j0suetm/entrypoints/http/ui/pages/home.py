from datetime import datetime

import fast_html as html
from starlette.requests import Request
from starlette.responses import HTMLResponse

from j0suetm.entrypoints.http.ui import document


def _meta(label: str, value: str) -> html.Tag:
    return html.span([html.span(label, class_="k"), value])


def _rail(num: str, name: str) -> html.Tag:
    return html.div(
        [html.span(num, class_="num"), html.span(name, class_="name")],
        class_="rail",
    )


def _contact_link(label: str, value: str, href: str, external: bool = False) -> html.Tag:
    attrs = {"target": "_blank", "rel": "noopener noreferrer"} if external else {}
    return html.a(
        [html.span(label, class_="label"), html.span(value, class_="val")],
        href=href,
        **attrs,
    )


def _top(years_working: int) -> html.Tag:
    return html.header(
        [
            html.div("Josué Teodoro Moreira", class_="wordmark"),
            html.div(
                [
                    _meta("Role", "Software Engineer"),
                    _meta("Experience", f"{years_working}+ years"),
                    _meta("Based", "Brazil"),
                ],
                class_="topmeta",
            ),
        ],
        class_="top",
    )


def _intro(years_working: int) -> html.Tag:
    return html.section(
        [
            _rail("01", "Index"),
            html.div(
                [
                    html.h1("Hi, I'm Josué."),
                    html.p(
                        "Backend / Distributed Systems / Reliability", class_="tags"
                    ),
                    html.p(f"""
                        I build software, mostly the parts you never see. For {years_working}+ years
                        I've worked on systems that quietly carry millions of people,
                        and the best compliment I get is no one noticing them.
                    """),
                    html.p("""
                        I have a soft spot for simple systems. I think most complexity is
                        accidental, and that good design is mostly subtraction: fewer moving
                        parts, clearer boundaries, state kept where it can't hurt you. A lot
                        of my work is just making complicated things boring.
                    """),
                ],
                class_="lede",
            ),
        ],
        class_="row intro",
    )


def _contact() -> html.Tag:
    return html.section(
        [
            _rail("02", "Contact"),
            html.div(
                [
                    html.p("Writing soon.", class_="muted"),
                    html.nav(
                        [
                            _contact_link(
                                "Email",
                                "hello@j0suetm.dev",
                                "mailto:hello@j0suetm.dev",
                            ),
                            _contact_link(
                                "GitHub",
                                "github.com/j0suetm",
                                "https://github.com/j0suetm",
                                external=True,
                            ),
                            _contact_link(
                                "LinkedIn",
                                "in/josue-teodoro-moreira",
                                "https://linkedin.com/in/josue-teodoro-moreira",
                                external=True,
                            ),
                        ],
                        class_="contacts",
                        aria_label="Contact",
                    ),
                ],
                class_="lede",
            ),
        ],
        class_="row contact",
    )


def _footer(cur_year: int) -> html.Tag:
    return html.footer(
        [html.span("J · T · M"), html.span(f"All rights reserved · {cur_year}")],
        class_="bottom",
    )


def render() -> html.Tag:
    began_working_at = 2021
    cur_year = datetime.now().year
    years_working = cur_year - began_working_at

    return html.div(
        [
            _top(years_working),
            html.main([_intro(years_working), _contact()]),
            _footer(cur_year),
        ],
        class_="frame",
    )


async def handle(_req: Request) -> HTMLResponse:
    return HTMLResponse(document.render([render()]))
