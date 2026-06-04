import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

    @property
    def environment(self):
        return os.getenv("ENVIRONMENT", "local")

    @property
    def is_prod(self):
        return self.environment == "prod"


global_cfg = Config()
