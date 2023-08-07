from app.repositories.submenu import SubmenuRepository


class SubmenuService:

    def __init__(self, database_repository: SubmenuRepository):
        self.database_repository = database_repository
