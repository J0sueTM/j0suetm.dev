from starlette.requests import Request
from starlette.responses import HTMLResponse

from j0suetm import infra
from j0suetm.services.inbound import fs_in, http_in
from j0suetm.services.outbound import fs_out


async def get_htmx_script(_req: Request) -> HTMLResponse:
    fs_script_fname = f"htmx.{infra.global_cfg.htmx_version}.min.js"
    fs_script = fs_in.get_script(fs_script_fname)
    if fs_script:
        return HTMLResponse(content=fs_script, media_type="text/javascript")

    cdn_script = http_in.get_htmx_script()
    fs_out.save_script(fs_script_fname, cdn_script)

    return HTMLResponse(content=cdn_script, media_type="text/javascript")
