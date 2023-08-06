from fastapi import Depends

from app.repositories.menu import MenuRepository


class MenuService:

    def __init__(self, database_repository: MenuRepository = Depends()):
        self.database_repository = database_repository
