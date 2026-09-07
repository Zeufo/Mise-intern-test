import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

CURRENT_FILE_PATH = Path(__file__).resolve()
SRC_DIR = next(p for p in CURRENT_FILE_PATH.parents if p.name == "src")
DOTENV_PATH = SRC_DIR.parent / ".env"


try:
    load_dotenv(dotenv_path=DOTENV_PATH)

    DB_NAME = os.getenv("DB_NAME")
    MAX_CAPACITY_PER_SLOT = os.getenv("MAX_CAPACITY_PER_SLOT")

    required_vars = {
        "DB_NAME": DB_NAME,
        "MAX_CAPACITY_PER_SLOT": MAX_CAPACITY_PER_SLOT,
    }

    DATABASE_URL = f"sqlite+aiosqlite:///{SRC_DIR}/{DB_NAME}"

    for var_name, var_value in required_vars.items():
        if var_value is None:
            logger.critical(f"{var_name} is not set")
            raise RuntimeError

    MAX_CAPACITY_PER_SLOT = int(MAX_CAPACITY_PER_SLOT)  # type: ignore

except Exception as e:
    logger.critical("cant load dotenv info", e)
    raise RuntimeError("cant load dotenv info")
