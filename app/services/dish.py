from app.repositories.dish import DishRepository


class DishService:

    def __init__(self, database_repository: DishRepository):
        self.database_repository = database_repository
