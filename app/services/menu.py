import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import menu_validator
from app.cache.cache_utils import clear_cache, get_cache, set_cache
from app.core.db import get_async_session
from app.models.menu import Menu
from app.repositories.menu import menu_crud_repository
from app.schemas.menu import MenuCreate, MenuUpdate
from app.schemas.status import StatusMessage


class MenuService:
    def __init__(self, session):
        self.session = session

    async def create_menu(self, menu_data: MenuCreate) -> Menu | HTTPException:
        """Create an instance of menu model and cache setup."""

        await menu_validator.check_title(menu_data.title, self.session)
        menu = await menu_crud_repository.create_instance(menu_data, self.session)
        await set_cache('menu', menu.id, menu)
        await clear_cache('menu', 'list')
        return menu

    async def get_menu(self, menu_id: uuid.UUID) -> Menu | HTTPException:
        """Get one instance of model by id and cache setup."""

        cached = await get_cache('menu', menu_id)
        if cached:
            return cached
        await menu_validator.check_exists(menu_id, self.session)
        menu = await menu_crud_repository.get_instance(menu_id, self.session)
        await set_cache('menu', menu_id, menu)
        return menu

    async def get_menu_list(self) -> list:
        """Get all instances of menu model and cache setup."""

        cached = await get_cache('menu', 'list')
        if cached:
            return cached
        menu_list = await menu_crud_repository.get_all_instances(self.session)
        await set_cache('menu', 'list', menu_list)
        return menu_list

    async def update_menu(
            self, menu_id: uuid.UUID, menu_data: MenuUpdate
    ) -> Menu | HTTPException:
        """Update the instance of menu model and cache setup."""

        menu_instance = await menu_validator.check_exists(
            menu_id, self.session)
        menu = await menu_crud_repository.update_instance(
            menu_instance, menu_data, self.session)
        await set_cache('menu', menu.id, menu)
        await clear_cache('menu', 'list')
        return menu

    async def delete_menu(self, menu_id) -> StatusMessage | HTTPException:
        """Delete the instance of menu model and cache setup"""

        menu_instance = await menu_validator.check_exists(
            menu_id, self.session)
        await menu_crud_repository.delete_instance(menu_instance, self.session)
        await clear_cache('menu', menu_id)
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True,
            message='The menu has been deleted',
        )

    async def get_all_data_menu(self, menu_id: uuid.UUID) -> list | HTTPException:
        """Get one instance of menu by id with all data."""

        await menu_validator.check_exists(menu_id, self.session)
        menu_data = await menu_crud_repository.get_all_data(menu_id, self.session)
        return menu_data


async def menu_service(session: AsyncSession = Depends(get_async_session)):
    return MenuService(session=session)
