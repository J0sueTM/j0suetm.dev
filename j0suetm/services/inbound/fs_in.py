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


def get_style(fname: str) -> bytes | None:
    styles_dir = infra.global_cfg.styles_dir.resolve()
    styles_dir.mkdir(parents=True, exist_ok=True)

    file = (styles_dir / fname).resolve()
    if not file.is_relative_to(styles_dir):
        LOGGER.warning("get_style.escapes_dir fname=%r", fname)
        return None

    if file.is_file():
        LOGGER.info("get_style.read fname=%r", fname)
        return file.read_bytes()

    LOGGER.warning("get_style.no_file fname=%r", fname)
    return None
