from utils import setup_logger


class Process:
    @staticmethod
    def prepare() -> None:
        setup_logger()
        pass

    @staticmethod
    async def run() -> None:
        pass
