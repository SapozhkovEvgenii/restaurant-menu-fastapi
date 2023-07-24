from fastapi import APIRouter

from app.api.endpoints import dish_router, menu_router, submenu_router

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(menu_router)
main_router.include_router(submenu_router)
main_router.include_router(dish_router)
