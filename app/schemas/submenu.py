import uuid
from pydantic import BaseModel


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    menu_id = uuid.UUID
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My submenu 1",
                "description": "My submenu description 1",
            },
        }


class SubMenuUpdate(SubMenuBase):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My updated submenu 1",
                "description": "My updated submenu description 1",
            },
        }


class SubMenuOut(SubMenuBase):
    id: uuid.UUID
    dishes_count: int

    class Config:
        from_attributes = True
