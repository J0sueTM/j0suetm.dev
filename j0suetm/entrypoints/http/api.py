from http import HTTPStatus

from starlette.requests import Request
from starlette.responses import JSONResponse


def get_health(_req: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy"}, status_code=HTTPStatus.OK)
