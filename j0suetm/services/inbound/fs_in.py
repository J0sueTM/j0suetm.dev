import logging

from j0suetm import infra

LOGGER = logging.getLogger(__name__)


def get_script(fname: str) -> bytes | None:
    infra.global_cfg.scripts_dir.mkdir(parents=True, exist_ok=True)

    file = infra.global_cfg.scripts_dir / fname
    if file.exists():
        LOGGER.info("get_script.read fname=%r", fname)
        return file.read_bytes()

    LOGGER.warning("get_script.no_file fname=%r", fname)
    return None
