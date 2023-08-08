import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import dish_validator
from app.cache.cache_utils import clear_cache, get_cache, set_cache
from app.core.db import get_async_session
from app.models.dish import Dish
from app.repositories.dish import dish_crud_repository
from app.schemas.dish import DishCreate, DishUpdate
from app.schemas.status import StatusMessage


class DishService:

    def __init__(self, session):
        self.session = session

    async def get_dish_list(
            self, submenu_id: uuid.UUID
    ) -> list:
        """Get all instances of dish model and cache setup."""

        cached = await get_cache(submenu_id, 'dish')
        if cached:
            return cached
        dish_list = await dish_crud_repository.get_all_subobjects(
            submenu_id, self.session)
        await set_cache(submenu_id, 'dish', dish_list)
        return dish_list

    async def get_dish(
            self, dish_id: uuid.UUID
    ) -> Dish | HTTPException:
        """Get one instance of dish model by id and cache setup."""

        cached = await get_cache('dish', dish_id)
        if cached:
            return cached
        await dish_validator.check_exists(dish_id, self.session)
        dish = await dish_crud_repository.get_instance(dish_id, self.session)
        await set_cache('dish', dish_id, dish)
        return dish

    async def create_dish(
            self,
            submenu_id: uuid.UUID,
            dish_data: DishCreate
    ) -> Dish | HTTPException:
        """Create an instance of dish model and cache setup."""

        await dish_validator.check_title(dish_data.title, self.session)
        dish = await dish_crud_repository.create_subobject(
            submenu_id,
            dish_data,
            self.session
        )
        await set_cache('dish', dish.id, dish)
        await clear_cache(submenu_id, 'dish')
        await clear_cache('submenu', submenu_id)
        await clear_cache('menu', 'list')
        return dish

    async def update_dish(
            self,
            dish_id: uuid.UUID,
            dish_data: DishUpdate
    ) -> Dish | HTTPException:
        """Update the instance of dish model and cache setup."""

        dish_instance = await dish_validator.check_exists(
            dish_id, self.session)
        dish = await dish_crud_repository.update_instance(
            dish_instance,
            dish_data,
            self.session
        )
        await set_cache('dish', dish_id, dish)
        await clear_cache(dish.parent_id, 'dish')
        await clear_cache('submenu', dish.parent_id)
        await clear_cache('menu', 'list')
        return dish

    async def delete_dish(
            self,
            dish_id: uuid.UUID
    ) -> StatusMessage | HTTPException:
        """Delete the instance of dish model and cache setup"""

        dish = await dish_validator.check_exists(dish_id, self.session)
        await dish_crud_repository.delete_instance(dish, self.session)
        await clear_cache('dish', dish_id)
        await clear_cache(dish.parent_id, 'dish')
        await clear_cache('menu', 'list')
        return StatusMessage(
            status=True,
            message='The dish has been deleted',
        )


async def dish_service(session: AsyncSession = Depends(get_async_session)):
    return DishService(session=session)
