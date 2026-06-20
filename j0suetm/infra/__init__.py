import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

    @property
    def environment(self) -> str:
        return os.getenv("ENVIRONMENT", "local")

    @property
    def is_prod(self) -> bool:
        return self.environment == "prod"

    @property
    def htmx_version(self) -> str:
        return "2.0.10"

    @property
    def root_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent.parent

    @property
    def scripts_dir(self) -> Path:
        return self.root_dir / "assets" / "scripts"


global_cfg = Config()
