import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.dish import DishCreate, DishOut, DishUpdate
from app.schemas.status import StatusMessage
from app.services.dish import DishService, dish_service

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
    service: DishService = Depends(dish_service)
) -> DishOut | HTTPException:
    """Create a new dish instatance."""

    return await service.create_dish(submenu_id, dish_in)


@router.get(
    '/{dish_id}',
    response_model=DishOut,
    status_code=HTTPStatus.OK,
)
async def get_dish(
    dish_id: uuid.UUID,
    service: DishService = Depends(dish_service)
) -> DishOut | HTTPException:
    """Get a dish instance by dish_id."""
    return await service.get_dish(dish_id)


@router.get(
    '/',
    response_model=list[DishOut],
    status_code=HTTPStatus.OK,
)
async def get_all_dishes(
    submenu_id: uuid.UUID,
    service: DishService = Depends(dish_service)
) -> list[DishOut]:
    """Get a list of all instances of a dish."""

    return await service.get_dish_list(submenu_id)


@router.patch(
    '/{dish_id}',
    response_model=DishOut,
    status_code=HTTPStatus.OK,
)
async def to_update_dish(
    dish_id: uuid.UUID,
    dish_in: DishUpdate,
    service: DishService = Depends(dish_service)
) -> DishOut | HTTPException:
    """Update a dish instance by dish_id."""

    return await service.update_dish(dish_id, dish_in)


@router.delete(
    '/{dish_id}',
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
)
async def to_delete_dish(
    dish_id: uuid.UUID,
    service: DishService = Depends(dish_service)
) -> StatusMessage | HTTPException:
    """Delete a dish instance by dish_id."""

    return await service.delete_dish(dish_id)
