import uuid

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from sqlalchemy import select

from app.schemas.status import StatusMessage

from .base import BaseRepository
from app.api.validators import menu_validator
from app.models.menu import Menu
from app.schemas.menu import MenuCreate, MenuUpdate


class MenuRepository(BaseRepository):

    async def create_menu(self, menu_in: MenuCreate) -> Menu | HTTPException:
        await menu_validator.check_title(menu_in.title, self.session)
        menu_in_data = menu_in.model_dump()
        menu = Menu(**menu_in_data)
        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)
        return menu

    async def get_menu(self, menu_id: uuid.UUID) -> Menu | HTTPException:
        await menu_validator.check_exists(menu_id, self.session)
        menu_obj = await self.session.execute(
            select(Menu).where(
                Menu.id == menu_id,
            ),
        )
        return menu_obj.scalars().first()

    async def get_menu_list(self) -> list:
        menu_objs = await self.session.execute(select(Menu))
        return menu_objs.scalars().all()

    async def update_menu(
            self, menu_id: uuid.UUID,
            menu_in: MenuUpdate) -> Menu | HTTPException:
        menu_obj = await menu_validator.check_exists(menu_id, self.session)
        obj_data = jsonable_encoder(menu_obj)
        update_data = menu_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(menu_obj, field, update_data[field])
        self.session.add(menu_obj)
        await self.session.commit()
        await self.session.refresh(menu_obj)
        return menu_obj

    async def delete_menu(
            self,
            menu_id: uuid.UUID) -> StatusMessage | HTTPException:
        menu_obj = await menu_validator.check_exists(menu_id, self.session)
        await self.session.delete(menu_obj)
        await self.session.commit()
        return StatusMessage(
            status=True,
            message="The menu has been deleted",
        )
