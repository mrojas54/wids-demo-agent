import logging
import os
import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import RegisterTortoise
from tortoise.contrib.test import MEMORY_SQLITE

from app import create_application
from app.config import Settings, get_settings
from app.routes import all_routes

ClientManagerType = AsyncGenerator[AsyncClient, None]

logger = logging.getLogger("cool.api.testing")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


def get_settings_override():
    return Settings(
        testing=1,
        environment="test",
        database_url=os.environ.get("DATABASE_TEST_URL", MEMORY_SQLITE),
        openai_api_key="test",
    )


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@asynccontextmanager
async def client_manager(app: FastAPI, base_url: str = "http://test", **kw) -> ClientManagerType:
    async with LifespanManager(app):
        transport = ASGITransport(app=app, client=("127.0.0.1", 8000))
        async with AsyncClient(transport=transport, base_url=base_url, **kw) as c:
            yield c


@pytest_asyncio.fixture(scope="function")
async def app():
    @asynccontextmanager
    async def lifespan_test(app: FastAPI) -> AsyncGenerator[None, None]:
        config = generate_config(
            os.environ.get("DATABASE_TEST_URL", MEMORY_SQLITE),
            app_modules={"models": ["app.models.tortoise"]},
            testing=True,
            connection_label="models",
        )
        async with RegisterTortoise(app=app, config=config, generate_schemas=True, _create_db=True):
            yield
        await Tortoise._drop_databases()

    app = create_application(lifespan_handler=lifespan_test, routes=all_routes)
    app.dependency_overrides[get_settings] = get_settings_override
    async with LifespanManager(app) as manager:
        logger.debug("Life span context manager started")
        yield manager.app
        logger.debug("Life span context manager stopped")


@pytest_asyncio.fixture(scope="function", autouse=True)
async def client(app: FastAPI) -> ClientManagerType:
    async with client_manager(app, base_url="http://test", follow_redirects=True) as c:
        yield c
