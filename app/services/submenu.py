import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from app.models.submenu import SubMenu
from .base import BaseService
from app.schemas.submenu import SubMenuCreate, SubMenuUpdate
from app.api.validators import submenu_validator
from app.schemas.status import StatusMessage


class SubmenuService(BaseService):

    async def create_submenu(
            self,
            menu_id: uuid.UUID,
            submenu_in: SubMenuCreate
    ):
        await submenu_validator.check_title(submenu_in.title, self.session)
        submenu_obj = SubMenu(
            title=submenu_in.title,
            description=submenu_in.description,
            parent_id=menu_id
        )
        self.session.add(submenu_obj)
        await self.session.commit()
        await self.session.refresh(submenu_obj)
        return submenu_obj

    async def get_submenu(self, submenu_id: uuid.UUID):
        await submenu_validator.check_exists(submenu_id, self.session)
        submenu_obj = await self.session.execute(
            select(SubMenu).where(
                SubMenu.id == submenu_id
            )
        )
        return submenu_obj.scalars().first()

    async def get_submenu_list(self):
        submenu_objs = await self.session.execute(select(SubMenu))
        return submenu_objs.scalars().all()

    async def update_submenu(
            self,
            submenu_id: uuid.UUID,
            submenu_in: SubMenuUpdate):
        submenu_obj = await submenu_validator.check_exists(submenu_id,
                                                           self.session)
        obj_data = jsonable_encoder(submenu_obj)
        update_data = submenu_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(submenu_obj, field, update_data[field])
        self.session.add(submenu_obj)
        await self.session.commit()
        await self.session.refresh(submenu_obj)
        return submenu_obj

    async def delete_submenu(self, submenu_id: uuid.UUID):
        submenu_obj = await submenu_validator.check_exists(submenu_id, self.session)
        await self.session.delete(submenu_obj)
        await self.session.commit()
        return StatusMessage(
            status=True,
            message="The submenu has been deleted",
        )
