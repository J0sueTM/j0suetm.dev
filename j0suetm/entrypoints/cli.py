import logging

import click
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route

from j0suetm import infra
from j0suetm.entrypoints.http import api, assets
from j0suetm.entrypoints.http.ui.pages import home

LOGGER = logging.getLogger(__name__)


def start_app() -> Starlette:
    return Starlette(
        debug=not infra.global_cfg.is_prod,
        routes=[
            Route("/", home.handle),
            Route("/assets/scripts/htmx.js", assets.get_htmx_script),
            Route("/assets/styles/{fname}", assets.get_style),
            Route("/api/health", api.get_health),
        ],
    )


@click.group()
def cli(): ...


@cli.command()
@click.option("--reload", "reload", default=False)
def serve(reload: bool) -> None:
    uvicorn.run(
        "j0suetm.entrypoints.cli:start_app",
        host="0.0.0.0",
        port=8000,
        reload=reload,
        factory=True,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cli()
