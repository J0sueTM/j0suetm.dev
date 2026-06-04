from starlette.applications import Starlette
from starlette.routing import Route

from j0suetm import infra
from j0suetm.entrypoints.http import api


def start_app() -> Starlette:
    return Starlette(
        debug=not infra.global_cfg.is_prod,
        routes=[
            Route("/api/health", api.get_health),
        ],
    )


app = start_app()
