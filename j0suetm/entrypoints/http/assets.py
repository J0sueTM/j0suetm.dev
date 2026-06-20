from starlette.requests import Request
from starlette.responses import Response

from j0suetm import infra
from j0suetm.domain import fingerprint
from j0suetm.services.inbound import fs_in, http_in
from j0suetm.services.outbound import fs_out

IMMUTABLE_CACHE = "public, max-age=31536000, immutable"


async def get_htmx_script(_req: Request) -> Response:
    fs_script_fname = f"htmx.{infra.global_cfg.htmx_version}.min.js"
    fs_script = fs_in.get_script(fs_script_fname)
    if fs_script:
        return Response(content=fs_script, media_type="text/javascript")

    cdn_script = http_in.get_htmx_script()
    fs_out.save_script(fs_script_fname, cdn_script)

    return Response(content=cdn_script, media_type="text/javascript")


async def get_style(req: Request) -> Response:
    requested = fingerprint.split_fingerprint(req.path_params["fname"])
    if not requested:
        return Response(status_code=404)

    fname, req_hash = requested
    style = fs_in.get_style(fname)
    if not style or fingerprint.content_hash(style) != req_hash:
        return Response(status_code=404)

    return Response(
        content=style,
        media_type="text/css",
        headers={"Cache-Control": IMMUTABLE_CACHE},
    )
