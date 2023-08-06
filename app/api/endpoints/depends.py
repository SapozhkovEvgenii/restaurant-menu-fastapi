from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.repositories.dish import DishRepository
from app.repositories.menu import MenuRepository
from app.repositories.submenu import SubmenuRepository


async def get_menu_repository(
        session: AsyncSession = Depends(get_async_session)
) -> MenuRepository:
    """
    Get a MenuRepository instance with a session.
    """
    return MenuRepository(session=session)


async def get_submenu_repository(
        session: AsyncSession = Depends(get_async_session)
) -> SubmenuRepository:
    """
    Get a SubmenuRepository instance with a session.
    """
    return SubmenuRepository(session=session)


async def get_dish_repository(
        session: AsyncSession = Depends(get_async_session)
) -> DishRepository:
    """
    Get a DishRepository instance with a session.
    """
    return DishRepository(session=session)
