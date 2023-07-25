from http import HTTPStatus
import uuid

from fastapi import APIRouter, Depends

from app.services.submenu import SubmenuService
from app.schemas.status import StatusMessage
from app.schemas.submenu import SubMenuCreate, SubMenuOut, SubMenuUpdate
from app.api.endpoints.depends import get_submenu_service

router = APIRouter(
    prefix="/menus/{menu_id}/submenus",
    tags=["Submenus"],
)


@router.post(
    "/",
    response_model=SubMenuOut,
    status_code=HTTPStatus.CREATED,
)
async def create_new_submenu(
    menu_id: uuid.UUID,
    submenu_in: SubMenuCreate,
    service: SubmenuService = Depends(get_submenu_service)
) -> SubMenuOut:

    return await service.create_submenu(menu_id, submenu_in)


@router.get(
    "/{submenu_id}",
    response_model=SubMenuOut,
    status_code=HTTPStatus.OK,
)
async def get_submenu(
    submenu_id: uuid.UUID,
    service: SubmenuService = Depends(get_submenu_service)
) -> SubMenuOut:
    return await service.get_submenu(submenu_id)


@router.get(
    "/",
    response_model=list[SubMenuOut],
    status_code=HTTPStatus.OK,
)
async def get_all_submenus(
    service: SubmenuService = Depends(get_submenu_service)
) -> list[SubMenuOut]:
    return await service.get_submenu_list()


@router.patch(
    "/{submenu_id}",
    response_model=SubMenuOut,
    status_code=HTTPStatus.OK,
)
async def to_update_submenu(
    submenu_id: uuid.UUID,
    submenu_in: SubMenuUpdate,
    service: SubmenuService = Depends(get_submenu_service)
) -> SubMenuOut:
    return await service.update_submenu(submenu_id, submenu_in)


@router.delete(
    "/{submenu_id}",
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
)
async def to_delete_menu(
    submenu_id: uuid.UUID,
    service: SubmenuService = Depends(get_submenu_service)
) -> StatusMessage:
    return await service.delete_submenu(submenu_id)
