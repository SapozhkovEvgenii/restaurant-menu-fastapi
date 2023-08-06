from http import HTTPStatus
import uuid

from fastapi import APIRouter, Depends

from app.services.dish import DishService
from app.schemas.status import StatusMessage
from app.schemas.dish import DishCreate, DishUpdate, DishOut
from app.api.endpoints.depends import get_dish_repository
from app.repositories.dish import DishRepository

router = APIRouter(
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"],
)


@router.post(
    "/",
    response_model=DishOut,
    status_code=HTTPStatus.CREATED,
)
async def create_new_dish(
    submenu_id: uuid.UUID,
    dish_in: DishCreate,
    service: DishService(DishRepository) = Depends(get_dish_repository)
) -> DishOut:
    """Create a new dish instatance."""

    return await service.create_dish(submenu_id, dish_in)


@router.get(
    "/{dish_id}",
    response_model=DishOut,
    status_code=HTTPStatus.OK,
)
async def get_dish(
    dish_id: uuid.UUID,
    service: DishService(DishRepository) = Depends(get_dish_repository)
) -> DishOut:
    """Get a dish instance by dish_id."""
    return await service.get_dish(dish_id)


@router.get(
    "/",
    response_model=list[DishOut],
    status_code=HTTPStatus.OK,
)
async def get_all_dishes(
    submenu_id: uuid.UUID,
    service: DishService(DishRepository) = Depends(get_dish_repository)
) -> list[DishOut]:
    """Get a list of all instances of a dish."""

    return await service.get_dish_list(submenu_id)


@router.patch(
    "/{dish_id}",
    response_model=DishOut,
    status_code=HTTPStatus.OK,
)
async def to_update_dish(
    dish_id: uuid.UUID,
    dish_in: DishUpdate,
    service: DishService(DishRepository) = Depends(get_dish_repository)
) -> DishOut:
    """Update a dish instance by dish_id."""

    return await service.update_dish(dish_id, dish_in)


@router.delete(
    "/{dish_id}",
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
)
async def to_delete_dish(
    dish_id: uuid.UUID,
    service: DishService(DishRepository) = Depends(get_dish_repository)
) -> StatusMessage:
    """Delete a dish instance by dish_id."""

    return await service.delete_dish(dish_id)
