import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.api.endpoints.depends import get_submenu_repository
from app.repositories.submenu import SubmenuRepository
from app.schemas.status import StatusMessage
from app.schemas.submenu import SubMenuCreate, SubMenuOut, SubMenuUpdate

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
    service: SubmenuRepository = Depends(get_submenu_repository)
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
    service: SubmenuRepository = Depends(get_submenu_repository)
) -> SubMenuOut | HTTPException:
    """Get a submenu instance by submenu_id"""

    return await service.get_submenu(submenu_id)


@router.get(
    '/',
    response_model=list[SubMenuOut],
    status_code=HTTPStatus.OK,
)
async def get_all_submenus(
    service: SubmenuRepository = Depends(get_submenu_repository)
) -> list[SubMenuOut]:
    """Get a list of all instances of a submenumenu."""

    return await service.get_submenu_list()


@router.patch(
    '/{submenu_id}',
    response_model=SubMenuOut,
    status_code=HTTPStatus.OK,
)
async def to_update_submenu(
    submenu_id: uuid.UUID,
    submenu_in: SubMenuUpdate,
    service: SubmenuRepository = Depends(get_submenu_repository)
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
    service: SubmenuRepository = Depends(get_submenu_repository)
) -> StatusMessage | HTTPException:
    """Delete a submenu instance by submenu_id"""

    return await service.delete_submenu(submenu_id)
