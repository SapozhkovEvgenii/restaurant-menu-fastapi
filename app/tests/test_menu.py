import json
import uuid
from http import HTTPStatus
from httpx import AsyncClient
from app.models import Menu


async def test_get_empty_menu_list(async_client: AsyncClient):

    """Request to the empty database"""

    response = await async_client.get('api/v1/menus/')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert response_data == []


async def test_create_menu(
        async_client: AsyncClient,
        get_object_from_database_by_uuid):

    """Creating a menu instance"""

    menu_data = {
        'title': 'My menu 1',
        'description': 'My menu description 1',
    }

    response = await async_client.post(
        '/api/v1/menus/',
        data=json.dumps(menu_data),
    )
    resp_data = response.json()
    assert response.status_code == HTTPStatus.CREATED
    assert resp_data['title'] == menu_data['title']
    assert resp_data['description'] == menu_data['description']
    assert resp_data['submenus_count'] == 0
    assert resp_data['dishes_count'] == 0
    menu_from_db = await get_object_from_database_by_uuid(Menu, resp_data['id'])
    assert len(menu_from_db) == 1
    menu_from_db = dict(menu_from_db[0])
    assert menu_from_db['title'] == resp_data['title']
    assert menu_from_db['description'] == resp_data['description']
    assert str(menu_from_db["id"]) == resp_data['id']


async def test_create_menu_invalid_title(
        async_client: AsyncClient,
        create_menu):

    """Creating a menu instance with invalid title"""

    menu_data = {
        'title': 'My menu 1',
        'description': 'My menu description 1',
    }

    response = await async_client.post(
        '/api/v1/menus/',
        data=json.dumps(menu_data),
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    response_data = response.json()
    assert response_data['detail'] == 'A menu with this name already exists'


async def test_get_menu_list(async_client: AsyncClient, create_menu):

    """Getting menu list"""

    response = await async_client.get("/api/v1/menus/")
    assert response.status_code == HTTPStatus.OK
    resp_data = response.json()
    assert isinstance(resp_data, list)
    assert len(resp_data) == 1


async def test_get_menu_by_id(
        async_client: AsyncClient,
        get_object_from_database_by_uuid,
        create_menu):

    """Getting menu by id"""

    id_response = await async_client.get(f'/api/v1/menus/{create_menu.id}')
    id_resp_data = id_response.json()
    assert id_response.status_code == HTTPStatus.OK
    assert id_resp_data['submenus_count'] == 0
    assert id_resp_data['dishes_count'] == 0
    menu_from_db = await get_object_from_database_by_uuid(Menu, id_resp_data['id'])
    assert len(menu_from_db) == 1
    menu_from_db = dict(menu_from_db[0])
    assert menu_from_db['title'] == id_resp_data['title']
    assert menu_from_db['description'] == id_resp_data['description']
    assert str(menu_from_db["id"]) == id_resp_data['id']


async def test_get_menu_not_found(async_client: AsyncClient):

    """GET request to a non-existent menu"""

    menu_id = uuid.uuid4()
    response = await async_client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    resp_data = response.json()
    assert resp_data['detail'] == 'menu not found'


async def test_update_menu(
        async_client: AsyncClient,
        get_object_from_database_by_uuid,
        create_menu):

    """Update menu"""

    updated_menu_data = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
    }

    patch_response = await async_client.patch(
        f'/api/v1/menus/{create_menu.id}',
        data=json.dumps(updated_menu_data),
    )
    patch_data = patch_response.json()
    assert patch_response.status_code == HTTPStatus.OK
    assert patch_data['title'] == updated_menu_data['title']
    assert patch_data['description'] == updated_menu_data['description']
    assert patch_data['submenus_count'] == 0
    assert patch_data['dishes_count'] == 0
    menu_from_db = await get_object_from_database_by_uuid(Menu, patch_data['id'])
    assert len(menu_from_db) == 1
    menu_from_db = dict(menu_from_db[0])
    assert menu_from_db['title'] == patch_data['title']
    assert menu_from_db['description'] == patch_data['description']
    assert str(menu_from_db["id"]) == patch_data['id']


async def test_update_menu_not_found(async_client: AsyncClient):

    """PATCH request to a non-existent menu"""

    updated_menu_data = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
    }

    menu_id = uuid.uuid4()
    response = await async_client.patch(
        f"/api/v1/menus/{menu_id}",
        data=json.dumps(updated_menu_data),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    resp_data = response.json()
    assert resp_data['detail'] == 'menu not found'


async def test_delete_menu(async_client: AsyncClient, create_menu):

    """Delete menu"""

    delete_response = await async_client.delete(f"/api/v1/menus/{create_menu.id}")
    delete_data = delete_response.json()
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_data['status'] is True
    assert delete_data['message'] == 'The menu has been deleted'


async def test_delete_menu_not_found(async_client: AsyncClient, create_menu):

    """Delete request to a non-existent menu"""

    menu_id = uuid.uuid4()
    delete_response = await async_client.get(f"/api/v1/menus/{menu_id}")
    assert delete_response.status_code == HTTPStatus.NOT_FOUND
    delete_data = delete_response.json()
    assert delete_data['detail'] == 'menu not found'
