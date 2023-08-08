import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.status import StatusMessage
from app.schemas.submenu import SubMenuCreate, SubMenuOut, SubMenuUpdate
from app.services.submenu import SubmenuService, submenu_service

router = APIRouter(
    prefix='/menus/{menu_id}/submenus',
    tags=['Submenus'],
)


@router.post(
    '/',
    response_model=SubMenuOut,
    status_code=HTTPStatus.CREATED,
)
async def create_new_submenu(
    menu_id: uuid.UUID,
    submenu_in: SubMenuCreate,
    service: SubmenuService = Depends(submenu_service)
) -> SubMenuOut | HTTPException:
    """Create a submenu instance"""

    return await service.create_submenu(menu_id, submenu_in)


@router.get(
    '/{submenu_id}',
    response_model=SubMenuOut,
    status_code=HTTPStatus.OK,
)
async def get_submenu(
    submenu_id: uuid.UUID,
    service: SubmenuService = Depends(submenu_service)
) -> SubMenuOut | HTTPException:
    """Get a submenu instance by submenu_id"""

    return await service.get_submenu(submenu_id)


@router.get(
    '/',
    response_model=list[SubMenuOut],
    status_code=HTTPStatus.OK,
)
async def get_all_submenus(
    menu_id: uuid.UUID,
    service: SubmenuService = Depends(submenu_service)
) -> list[SubMenuOut]:
    """Get a list of all instances of a submenumenu."""

    return await service.get_submenu_list(menu_id)


@router.patch(
    '/{submenu_id}',
    response_model=SubMenuOut,
    status_code=HTTPStatus.OK,
)
async def to_update_submenu(
    submenu_id: uuid.UUID,
    submenu_in: SubMenuUpdate,
    service: SubmenuService = Depends(submenu_service)
) -> SubMenuOut | HTTPException:
    """Update a submenu instance by submenu_id"""

    return await service.update_submenu(submenu_id, submenu_in)


@router.delete(
    '/{submenu_id}',
    response_model=StatusMessage,
    status_code=HTTPStatus.OK,
)
async def to_delete_menu(
    submenu_id: uuid.UUID,
    service: SubmenuService = Depends(submenu_service)
) -> StatusMessage | HTTPException:
    """Delete a submenu instance by submenu_id"""

    return await service.delete_submenu(submenu_id)
