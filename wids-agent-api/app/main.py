import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import (
    tortoise_exception_handlers,
)
from app import create_application
from app.routes import all_routes
from app.dependencies.db import register_orm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cool.api")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting up...")
    async with register_orm(app):
        yield
    logger.info("Shutting down...")


app = create_application(
    lifespan_handler=lifespan,
    exception_handlers=tortoise_exception_handlers(),
    routes=all_routes,
)
