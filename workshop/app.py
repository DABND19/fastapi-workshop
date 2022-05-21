from fastapi import FastAPI

from workshop.api import router
from workshop.config import settings


def get_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router)

    return app
