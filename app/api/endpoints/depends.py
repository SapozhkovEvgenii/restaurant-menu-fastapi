from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.menu import MenuService
from app.core.db import get_async_session


async def get_menu_service(session: AsyncSession = Depends(get_async_session)):
    return MenuService(session=session)
