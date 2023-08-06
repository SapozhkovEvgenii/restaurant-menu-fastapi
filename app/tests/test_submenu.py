import json
import uuid
from http import HTTPStatus

from httpx import AsyncClient

from app.models import SubMenu


async def test_get_empty_submenu_list(
        async_client: AsyncClient,
        create_menu):

    """Request to the empty database"""

    response = await async_client.get(f'/api/v1/menus/{create_menu.id}/submenus/')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data == []


async def test_create_submenu(
        async_client: AsyncClient,
        get_object_from_database_by_uuid,
        create_menu):

    """Creating a submenu instance"""

    submenu_data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
    }

    response = await async_client.post(
        f'/api/v1/menus/{create_menu.id}/submenus/',
        data=json.dumps(submenu_data),
    )
    resp_data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert resp_data['title'] == submenu_data['title']
    assert resp_data['description'] == submenu_data['description']
    assert resp_data['dishes_count'] == 0
    submenu_from_db = await get_object_from_database_by_uuid(SubMenu, resp_data['id'])
    assert len(submenu_from_db) == 1
    submenu_from_db = dict(submenu_from_db[0])
    assert submenu_from_db['title'] == resp_data['title']
    assert submenu_from_db['description'] == resp_data['description']
    assert str(submenu_from_db['id']) == resp_data['id']


async def test_create_submenu_invalid_title(
        async_client: AsyncClient,
        create_submenu):

    """Creating a submenu instance with invalid title"""

    submenu_data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
    }

    response = await async_client.post(
        f'/api/v1/menus/{create_submenu.parent_id}/submenus/',
        data=json.dumps(submenu_data),
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert response_data['detail'] == 'A submenu with this name already exists'


async def test_get_submenu_list(async_client: AsyncClient, create_submenu):

    """Getting submenu list"""

    response = await async_client.get(f'/api/v1/menus/{create_submenu.parent_id}/submenus/')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1


async def test_get_submenu_by_id(
        async_client: AsyncClient,
        get_object_from_database_by_uuid,
        create_submenu):

    """Getting submenu by id"""

    id_response = await async_client.get(
        f'/api/v1/menus/{create_submenu.parent_id}/submenus/{create_submenu.id}'
    )
    id_resp_data = id_response.json()
    assert id_response.status_code == HTTPStatus.OK
    assert id_resp_data['dishes_count'] == 0
    submenu_from_db = await get_object_from_database_by_uuid(
        SubMenu,
        id_resp_data['id'])
    assert len(submenu_from_db) == 1
    submenu_from_db = dict(submenu_from_db[0])
    assert submenu_from_db['title'] == id_resp_data['title']
    assert submenu_from_db['description'] == id_resp_data['description']
    assert str(submenu_from_db['id']) == id_resp_data['id']


async def test_get_submenu_not_found(async_client: AsyncClient, create_menu):

    """GET request to a non-existent submenu"""

    submenu_id = uuid.uuid4()
    response = await async_client.get(
        f'/api/v1/menus/{create_menu.id}/submenus/{submenu_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    resp_data = response.json()
    assert resp_data['detail'] == 'submenu not found'


async def test_update_submenu(
        async_client: AsyncClient,
        get_object_from_database_by_uuid,
        create_submenu):

    """Update submenu"""

    updated_submenu_data = {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1',
    }

    patch_response = await async_client.patch(
        f'/api/v1/menus/{create_submenu.parent_id}/submenus/{create_submenu.id}',
        data=json.dumps(updated_submenu_data),
    )
    patch_data = patch_response.json()
    assert patch_response.status_code == HTTPStatus.OK
    assert patch_data['title'] == updated_submenu_data['title']
    assert patch_data['description'] == updated_submenu_data['description']
    assert patch_data['dishes_count'] == 0
    submenu_from_db = await get_object_from_database_by_uuid(SubMenu, patch_data['id'])
    assert len(submenu_from_db) == 1
    submenu_from_db = dict(submenu_from_db[0])
    assert submenu_from_db['title'] == patch_data['title']
    assert submenu_from_db['description'] == patch_data['description']
    assert str(submenu_from_db['id']) == patch_data['id']


async def test_update_submenu_not_found(async_client: AsyncClient, create_menu):

    """PATCH request to a non-existent submenu"""

    updated_submenu_data = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
    }

    submenu_id = uuid.uuid4()
    response = await async_client.patch(
        f'/api/v1/menus/{create_menu.id}/submenus/{submenu_id}',
        data=json.dumps(updated_submenu_data),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    resp_data = response.json()
    assert resp_data['detail'] == 'submenu not found'


async def test_delete_submenu(async_client: AsyncClient, create_submenu):

    """Delete submenu"""

    delete_response = await async_client.delete(
        f'/api/v1/menus/{create_submenu.parent_id}/submenus/{create_submenu.id}')
    delete_data = delete_response.json()
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_data['status'] is True
    assert delete_data['message'] == 'The submenu has been deleted'


async def test_delete_submenu_not_found(async_client: AsyncClient, create_menu):

    """Delete request to a non-existent submenu"""

    submenu_id = uuid.uuid4()
    delete_response = await async_client.get(
        f'/api/v1/menus/{create_menu.id}/submenus/{submenu_id}')
    assert delete_response.status_code == HTTPStatus.NOT_FOUND
    delete_data = delete_response.json()
    assert delete_data['detail'] == 'submenu not found'
