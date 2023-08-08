import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import submenu_validator
from app.cache.cache_utils import clear_cache, get_cache, set_cache
from app.core.db import get_async_session
from app.models.submenu import SubMenu
from app.repositories.submenu import submenu_crud_repository
from app.schemas.status import StatusMessage
from app.schemas.submenu import SubMenuCreate, SubMenuUpdate


class SubmenuService:

    def __init__(self, session):
        self.session = session

    async def create_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_data: SubMenuCreate
    ) -> SubMenu | HTTPException:
        """Create an instance of submenu model and cache setup."""

        await submenu_validator.check_title(submenu_data.title, self.session)
        submenu = await submenu_crud_repository.create_subobject(
            menu_id, submenu_data, self.session)
        await set_cache('submenu', submenu.id, submenu)
        await clear_cache('menu', menu_id)
        await clear_cache('menu', 'list')
        return submenu

    async def get_submenu(
            self, submenu_id: uuid.UUID) -> SubMenu | HTTPException:
        """Get one instance of model by id and cache setup."""

        cached = await get_cache('submenu', submenu_id)
        if cached:
            return cached
        await submenu_validator.check_exists(submenu_id, self.session)
        submenu = await submenu_crud_repository.get_instance(
            submenu_id, self.session)
        await set_cache('submenu', submenu_id, submenu)
        return submenu

    async def get_submenu_list(self, menu_id: uuid.UUID) -> list:
        """Get all instances of submenu model and cache setup."""

        cached = await get_cache(menu_id, 'submenu')
        if cached:
            return cached
        submenu_list = await submenu_crud_repository.get_all_subobjects(
            menu_id, self.session)
        await set_cache(menu_id, 'submenu', submenu_list)
        return submenu_list

    async def update_submenu(
            self,
            submenu_id: uuid.UUID,
            submenu_data: SubMenuUpdate
    ) -> SubMenu | HTTPException:
        """Update the instance of submenu model and cache setup."""

        submenu_instance = await submenu_validator.check_exists(
            submenu_id, self.session)
        submenu = await submenu_crud_repository.update_instance(
            submenu_instance,
            submenu_data,
            self.session
        )
        await set_cache('submenu', submenu_id, submenu)
        await clear_cache(submenu.parent_id, 'submenu')
        await clear_cache('menu', submenu.parent_id)
        await clear_cache('menu', 'list')
        return submenu

    async def delete_submenu(
            self,
            submenu_id: uuid.UUID
    ) -> StatusMessage | HTTPException:
        """Delete the instance of submenu model and cache setup"""

        submenu = await submenu_validator.check_exists(
            submenu_id, self.session)
        await submenu_crud_repository.delete_instance(
            submenu, self.session)
        await clear_cache('submenu', submenu_id)
        await clear_cache(submenu.parent_id, 'submenu')
        await clear_cache('menu', submenu.parent_id)
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True,
            message='The submenu has been deleted',
        )


async def submenu_service(session: AsyncSession = Depends(get_async_session)):
    return SubmenuService(session=session)
