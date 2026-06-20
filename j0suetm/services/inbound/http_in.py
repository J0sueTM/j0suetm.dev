import logging

import httpx

LOGGER = logging.getLogger(__name__)


def get_htmx_script() -> bytes:
    resp = httpx.get("https://cdn.jsdelivr.net/npm/htmx.org@2.0.10/dist/htmx.min.js")
    resp.raise_for_status()
    return resp.content
