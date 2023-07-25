import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.api.endpoints.depends import get_menu_service
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
    menu: MenuCreate, service: MenuService = Depends(get_menu_service)
) -> MenuOut:

    return await service.create_menu(menu)


@router.get(
    "/{menu_id}",
    response_model=MenuOut,
    status_code=HTTPStatus.OK,
)
async def get_menu(
    menu_id: uuid.UUID, service: MenuService = Depends(get_menu_service)
) -> MenuOut:
    return await service.get_menu(menu_id)


@router.get(
    "/",
    response_model=list[MenuOut],
    status_code=HTTPStatus.OK,
)
async def get_all_menus(service: MenuService = Depends(get_menu_service)) -> list[MenuOut]:
    return await service.get_menu_list()


@router.patch(
    "/{menu_id}",
    response_model=MenuOut,
    status_code=HTTPStatus.OK,
)
async def to_update_menu(
    menu_id: uuid.UUID, obj_in: MenuUpdate, service: MenuService = Depends(get_menu_service)
) -> MenuOut:
    return await service.update_menu(menu_id, obj_in)


@router.delete(
    "/{menu_id}",
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
)
async def to_delete_menu(
    menu_id: uuid.UUID, service: MenuService = Depends(get_menu_service)
) -> StatusMessage:
    return await service.delete_menu(menu_id)
