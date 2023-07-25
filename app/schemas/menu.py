import uuid
from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My menu 1",
                "description": "My menu description 1",
            },
        }


class MenuUpdate(MenuBase):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My updated menu 1",
                "description": "My updated menu description 1",
            },
        }


class MenuOut(MenuBase):
    id: uuid.UUID
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True
