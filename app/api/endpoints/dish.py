import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.api.endpoints.depends import get_dish_repository
from app.repositories.dish import DishRepository
from app.schemas.dish import DishCreate, DishOut, DishUpdate
from app.schemas.status import StatusMessage
from app.services.dish import DishService

router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dishes'],
)


@router.post(
    '/',
    response_model=DishOut,
    status_code=HTTPStatus.CREATED,
)
async def create_new_dish(
    submenu_id: uuid.UUID,
    dish_in: DishCreate,
    service=DishService(DishRepository(Depends(get_dish_repository)))
) -> DishOut | HTTPException:
    """Create a new dish instatance."""

    return await service.database_repository.create_dish(submenu_id, dish_in)


@router.get(
    '/{dish_id}',
    response_model=DishOut,
    status_code=HTTPStatus.OK,
)
async def get_dish(
    dish_id: uuid.UUID,
    service=DishService(DishRepository(Depends(get_dish_repository)))
) -> DishOut | HTTPException:
    """Get a dish instance by dish_id."""
    return await service.database_repository.get_dish(dish_id)


@router.get(
    '/',
    response_model=list[DishOut],
    status_code=HTTPStatus.OK,
)
async def get_all_dishes(
    submenu_id: uuid.UUID,
    service=DishService(DishRepository(Depends(get_dish_repository)))
) -> list[DishOut]:
    """Get a list of all instances of a dish."""

    return await service.database_repository.get_dish_list(submenu_id)


@router.patch(
    '/{dish_id}',
    response_model=DishOut,
    status_code=HTTPStatus.OK,
)
async def to_update_dish(
    dish_id: uuid.UUID,
    dish_in: DishUpdate,
    service=DishService(DishRepository(Depends(get_dish_repository)))
) -> DishOut | HTTPException:
    """Update a dish instance by dish_id."""

    return await service.database_repository.update_dish(dish_id, dish_in)


@router.delete(
    '/{dish_id}',
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
)
async def to_delete_dish(
    dish_id: uuid.UUID,
    service=DishService(DishRepository(Depends(get_dish_repository)))
) -> StatusMessage | HTTPException:
    """Delete a dish instance by dish_id."""

    return await service.database_repository.delete_dish(dish_id)
