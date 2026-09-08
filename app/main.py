from contextlib import asynccontextmanager

from api.booking import router
from core import setup_logger
from database import database_init
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    await database_init()
    yield


app = FastAPI(title="MISE Booking API", lifespan=lifespan)
app.include_router(router)
