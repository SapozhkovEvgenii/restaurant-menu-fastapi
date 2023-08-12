import uuid
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Menu, SubMenu
from app.repositories.base import BaseRepository


class MenuRepository(BaseRepository):

    async def get_all_data(self, instance_id: uuid.UUID, session: AsyncSession) -> Any:
        """Receive all menu data with all submenus with their dishes."""

        result = await session.scalars(
            select(self.model
                   ).where(self.model.id == instance_id,
                           ).options(
                joinedload(self.model.submenus).joinedload(SubMenu.dishes)
            )
        )
        menus = result.unique().all()
        menu_data = jsonable_encoder(menus)
        return menu_data


menu_crud_repository = MenuRepository(Menu)  # type: ignore
