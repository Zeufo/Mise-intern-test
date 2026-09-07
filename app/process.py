from database import database_init
from utils import setup_logger


class Process:
    @staticmethod
    def prepare() -> None:
        setup_logger()
        database_init()

    @staticmethod
    async def run() -> None:
        pass
