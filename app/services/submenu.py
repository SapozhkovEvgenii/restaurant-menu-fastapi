from fastapi import Depends

from app.repositories.submenu import SubmenuRepository


class SubmenuService:

    def __init__(self, database_repository: SubmenuRepository = Depends()):
        self.database_repository = database_repository
