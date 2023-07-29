import asyncio
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import TEST_ASYNC_DATABASE_URL
from app.core.db import Base, get_async_session
from app.main import app


async_engine = create_async_engine(TEST_ASYNC_DATABASE_URL, echo=True)

TestSession = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def get_test_db():
    async with TestSession() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    app.dependency_overrides[get_async_session] = get_test_db
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
