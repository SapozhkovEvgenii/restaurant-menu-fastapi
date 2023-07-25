from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dish, Menu, SubMenu


class Validation:
    def __init__(self, model):
        self.model = model

    async def check_exists(
        self,
        obj_id: str,
        session: AsyncSession,
    ):
        model_name = self.model.__tablename__
        obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id,
            ),
        )
        obj = obj.scalars().first()
        if obj is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"{model_name} not found",
            )
        return obj

    async def check_title(
        self,
        obj_title: str,
        session: AsyncSession,
    ):
        model_name = self.model.__tablename__
        obj_id = await session.execute(
            select(self.model.id).where(
                self.model.title == obj_title,
            ),
        )
        obj_id = obj_id.scalars().first()
        if obj_id is not None:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=f"A {model_name} with this name already exists",
            )
        return obj_id


menu_validator = Validation(Menu)
submenu_validator = Validation(SubMenu)
dish_validator = Validation(Dish)
