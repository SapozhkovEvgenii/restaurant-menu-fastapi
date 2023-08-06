import uuid

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from sqlalchemy import select

from .base import BaseRepository
from app.models.dish import Dish
from app.schemas.dish import DishCreate, DishUpdate
from app.api.validators import dish_validator
from app.schemas.status import StatusMessage


class DishRepository(BaseRepository):

    async def create_dish(
            self,
            submenu_id: uuid.UUID,
            dish_in: DishCreate) -> Dish | HTTPException:
        await dish_validator.check_title(dish_in.title, self.session)
        dish_in_data = dish_in.model_dump()
        dish_obj = Dish(
            ** dish_in_data,
            parent_id=submenu_id
        )
        self.session.add(dish_obj)
        await self.session.commit()
        await self.session.refresh(dish_obj)
        return dish_obj

    async def get_dish(self, dish_id: uuid.UUID) -> Dish | HTTPException:
        await dish_validator.check_exists(dish_id, self.session)
        dish_obj = await self.session.execute(
            select(Dish).where(
                Dish.id == dish_id
            )
        )
        return dish_obj.scalars().first()

    async def get_dish_list(self, submenu_id: uuid.UUID) -> list:
        dish_objs = await self.session.execute(
            select(Dish).where(Dish.parent_id == submenu_id))
        return dish_objs.scalars().all()

    async def update_dish(
            self,
            dish_id: uuid.UUID,
            dish_in: DishUpdate) -> Dish | HTTPException:
        dish_obj = await dish_validator.check_exists(dish_id,
                                                     self.session)
        obj_data = jsonable_encoder(dish_obj)
        update_data = dish_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(dish_obj, field, update_data[field])
        self.session.add(dish_obj)
        await self.session.commit()
        await self.session.refresh(dish_obj)
        return dish_obj

    async def delete_dish(
            self,
            submenu_id: uuid.UUID) -> StatusMessage | HTTPException:
        dish_obj = await dish_validator.check_exists(submenu_id, self.session)
        await self.session.delete(dish_obj)
        await self.session.commit()
        return StatusMessage(
            status=True,
            message="The dish has been deleted",
        )
