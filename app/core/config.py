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

    required_vars = {
        "DB_NAME": DB_NAME,
    }

    DATABASE_URL = f"sqlite+aiosqlite:///{SRC_DIR}/{DB_NAME}"

    for var_name, var_value in required_vars.items():
        if var_value is None:
            logger.critical(f"{var_name} is not set")
            raise RuntimeError

except Exception as e:
    logger.critical("cant load dotenv info", e)
    raise RuntimeError("cant load dotenv info")
