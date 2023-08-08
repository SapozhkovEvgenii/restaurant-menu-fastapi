from app.models.submenu import SubMenu

from .base import BaseRepository


class SubmenuRepository(BaseRepository):
    pass


submenu_crud_repository = SubmenuRepository(SubMenu)  # type: ignore
