import asyncio

from loguru import logger
from process import Process


async def main() -> None:
    Process.prepare()
    await Process.run()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.critical("keyboard interrupt!")
