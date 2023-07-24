from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from .base import BaseService
from api.validators import menu_validator
from models.menu import Menu
from schemas.menu import MenuCreate, MenuUpdate


class MenuService(BaseService):

    async def create_menu(self, menu_in: MenuCreate):
        await menu_validator.check_title(menu_in.title, self.session)
        menu = Menu(
            title=menu_in.title,
            description=menu_in.description
        )
        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)
        return menu

    async def get_menu(self, menu_id: str):
        await menu_validator.check_exists(menu_id, self.session)
        menu_obj = await self.session.execute(
            select(Menu).where(
                Menu.id == menu_id,
            ),
        )
        return menu_obj.scalars().first()

    async def get_menu_list(self):
        menu_objs = await self.session.execute(select(Menu))
        return menu_objs.scalars()

    async def update_menu(self, menu_id: str, menu_in: MenuUpdate):
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

    async def delete_menu(self, menu_id: str):
        menu_obj = await menu_validator.check_exists(menu_id, self.session)
        await self.session.delete(menu_obj)
        await self.session.commit()
        return menu_obj
