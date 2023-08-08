from app.models import Menu

from .base import BaseRepository


class MenuRepository(BaseRepository):
    pass


menu_crud_repository = MenuRepository(Menu)  # type: ignore
