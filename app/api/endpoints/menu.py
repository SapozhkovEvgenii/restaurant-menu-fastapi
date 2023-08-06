import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.api.endpoints.depends import get_menu_repository
from app.repositories.menu import MenuRepository
from app.services.menu import MenuService
from app.schemas.menu import MenuCreate, MenuOut, MenuUpdate
from app.schemas.status import StatusMessage

router = APIRouter(
    prefix="/menus",
    tags=["Menus"],
)


@router.post(
    "/",
    response_model=MenuOut,
    status_code=HTTPStatus.CREATED,
)
async def create_new_menu(
    menu: MenuCreate,
    service: MenuService(MenuRepository) = Depends(get_menu_repository)
) -> MenuOut:
    """Create a new menu instatance."""

    return await service.create_menu(menu)


@router.get(
    "/{menu_id}",
    response_model=MenuOut,
    status_code=HTTPStatus.OK,
)
async def get_menu(
    menu_id: uuid.UUID,
    service: MenuService(MenuRepository) = Depends(get_menu_repository)
) -> MenuOut:
    """Get a menu instance by dish_id."""

    return await service.get_menu(menu_id)


@router.get(
    "/",
    response_model=list[MenuOut],
    status_code=HTTPStatus.OK,
)
async def get_all_menus(
    service: MenuService(MenuRepository) = Depends(get_menu_repository)
) -> list[MenuOut]:
    """Get a list of all instances of a menu."""

    return await service.get_menu_list()


@router.patch(
    "/{menu_id}",
    response_model=MenuOut,
    status_code=HTTPStatus.OK,
)
async def to_update_menu(
    menu_id: uuid.UUID,
    obj_in: MenuUpdate,
    service: MenuService(MenuRepository) = Depends(get_menu_repository)
) -> MenuOut:
    """Update a menu instance by menu_id."""

    return await service.update_menu(menu_id, obj_in)


@router.delete(
    "/{menu_id}",
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
)
async def to_delete_menu(
    menu_id: uuid.UUID,
    service: MenuService(MenuRepository) = Depends(get_menu_repository)
) -> StatusMessage:
    """Delete a menu instance by menu_id."""

    return await service.delete_menu(menu_id)
