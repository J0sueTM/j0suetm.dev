import logging

from j0suetm import infra

LOGGER = logging.getLogger(__name__)


def save_script(fname: str, content: bytes) -> None:
    infra.global_cfg.scripts_dir.mkdir(parents=True, exist_ok=True)

    file = infra.global_cfg.scripts_dir / fname
    file.write_bytes(content)

    LOGGER.info("save_script.saved fname=%r", fname)
