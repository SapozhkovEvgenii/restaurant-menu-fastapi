import pytest
import json
from http import HTTPStatus
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_empty_menu_list(async_client: AsyncClient):

    """Request to the empty database"""

    response = await async_client.get('api/v1/menus/')
    print(response, '######################', end='\n\n\n')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    print(response, '######################', end='\n\n\n')
    assert response_data == []
