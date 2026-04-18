from collections.abc import AsyncGenerator, AsyncIterator, Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from tortoise.context import TortoiseContext
from tortoise.contrib.test import tortoise_test_context

from app.main import app


@pytest_asyncio.fixture
async def db() -> AsyncIterator[TortoiseContext]:
    async with tortoise_test_context(['app.models']) as ctx:
        yield ctx


@pytest.fixture
def test_client() -> Generator[TestClient]:
    test_app = FastAPI()
    test_app.routes.extend(app.routes)
    with TestClient(app=test_app) as client:
        yield client


@pytest_asyncio.fixture
async def apiclient() -> AsyncGenerator[AsyncClient]:
    async with tortoise_test_context(['app.models']) as _:
        test_app = FastAPI()
        test_app.routes.extend(app.routes)
        async with AsyncClient(transport=ASGITransport(app=test_app), base_url='http://fast-tortoise') as client:
            yield client
