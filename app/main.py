from fastapi import FastAPI

from app.api.routers import main_router

app = FastAPI(title='Restaurant menu')

app.include_router(main_router)
