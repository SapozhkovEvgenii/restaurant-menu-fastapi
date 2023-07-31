import json
import uuid
from httpx import AsyncClient
from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.core.config import TEST_ASYNC_DATABASE_URL
from sqlalchemy.orm import sessionmaker

from app.models import Dish
from app.models.menu import Menu


async def test_get_empty_dish_list(
        async_client: AsyncClient,
        create_submenu):

    """Request to the empty database"""

    response = await async_client.get(
        f'/api/v1/menus/{create_submenu.parent_id}/submenus/{create_submenu.id}/dishes/')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data == []


async def test_create_dish(
        async_client: AsyncClient,
        get_object_from_database_by_uuid,
        create_submenu):

    """Creating a dish instance"""

    dish_data = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50",
    }

    response = await async_client.post(
        f'/api/v1/menus/{create_submenu.parent_id}/submenus/{create_submenu.id}/dishes/',
        data=json.dumps(dish_data),
    )
    resp_data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert resp_data['title'] == dish_data['title']
    assert resp_data['description'] == dish_data['description']
    assert resp_data['price'] == dish_data['price']
    dish_from_db = await get_object_from_database_by_uuid(Dish, resp_data['id'])
    assert len(dish_from_db) == 1
    dish_from_db = dict(dish_from_db[0])
    assert dish_from_db['title'] == resp_data['title']
    assert dish_from_db['description'] == resp_data['description']
    assert dish_from_db['price'] == resp_data['price']
    assert str(dish_from_db["id"]) == resp_data['id']


async def test_create_dish_invalid_title(
        async_client: AsyncClient,
        create_dish):

    """Creating a dish instance with invalid title"""

    dish_data = {
        "title": "My dish 1",
        "description": "My dish description 2",
        "price": "22.50",
    }

    async_engine = create_async_engine(TEST_ASYNC_DATABASE_URL, echo=True)

    Session = sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with Session() as session:
        menu = await session.execute(select(Menu))
        menu_id = menu.scalars().first()

    response = await async_client.post(
        f'/api/v1/menus/{menu_id}/submenus/{create_dish.parent_id}/dishes/',
        data=json.dumps(dish_data),
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert response_data['detail'] == 'A dish with this name already exists'


async def test_get_dish_list(async_client: AsyncClient, create_dish):

    """Getting dish list"""

    async_engine = create_async_engine(TEST_ASYNC_DATABASE_URL, echo=True)

    Session = sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with Session() as session:
        menu = await session.execute(select(Menu))
        menu_id = menu.scalars().first()

    response = await async_client.get(
        f'/api/v1/menus/{menu_id}/submenus/{create_dish.parent_id}/dishes/')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1


async def test_get_dish_by_id(
        async_client: AsyncClient,
        get_object_from_database_by_uuid,
        create_dish):

    """Getting submenu by id"""

    async_engine = create_async_engine(TEST_ASYNC_DATABASE_URL, echo=True)

    Session = sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with Session() as session:
        menu = await session.execute(select(Menu))
        menu_id = menu.scalars().first()

    id_response = await async_client.get(
        f'/api/v1/menus/{menu_id}/submenus/{create_dish.parent_id}/dishes/{create_dish.id}'
    )
    id_resp_data = id_response.json()
    assert id_response.status_code == HTTPStatus.OK
    dish_from_db = await get_object_from_database_by_uuid(
        Dish,
        id_resp_data['id'])
    assert len(dish_from_db) == 1
    dish_from_db = dict(dish_from_db[0])
    assert dish_from_db['title'] == id_resp_data['title']
    assert dish_from_db['description'] == id_resp_data['description']
    assert dish_from_db['price'] == id_resp_data['price']
    assert str(dish_from_db["id"]) == id_resp_data['id']


