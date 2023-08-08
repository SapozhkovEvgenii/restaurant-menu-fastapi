from app.models import Dish

from .base import BaseRepository


class DishRepository(BaseRepository):
    pass


dish_crud_repository = DishRepository(Dish)  # type: ignore
