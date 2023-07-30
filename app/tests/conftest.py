import asyncio
from typing import Generator
import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import TEST_ASYNC_DATABASE_URL
from app.core.db import Base, get_async_session
from app.main import app
from app.models import Menu, SubMenu


async_engine = create_async_engine(TEST_ASYNC_DATABASE_URL, echo=True)

TestSession = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def get_test_db() -> AsyncSession:
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
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client


@pytest_asyncio.fixture
async def create_menu():
    menu_data = {
        'title': 'My menu 1',
        'description': 'My menu description 1',
    }

    async_engine = create_async_engine(TEST_ASYNC_DATABASE_URL, echo=True)

    Session = sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with Session() as session:
        menu_obj = Menu(**menu_data)
        session.add(menu_obj)
        await session.commit()
    return menu_obj


@pytest_asyncio.fixture
async def create_submenu(create_menu):
    submenu_data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
    }

    async_engine = create_async_engine(TEST_ASYNC_DATABASE_URL, echo=True)

    Session = sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with Session() as session:
        submenu_obj = SubMenu(**submenu_data, parent_id=create_menu.id)
        session.add(submenu_obj)
        await session.commit()
    return submenu_obj


@pytest_asyncio.fixture
async def get_object_from_database_by_uuid():
    async def get_object_from_database_by_uuid(obj: Base, id: uuid):
        async with async_engine.begin() as conn:
            obj = await conn.execute(select(obj).where(obj.id == id))
            result = obj.fetchall()
            return result
    return get_object_from_database_by_uuid
