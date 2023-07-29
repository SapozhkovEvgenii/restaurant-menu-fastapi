import uuid
from pydantic import BaseModel, ConfigDict


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "My menu 1",
            "description": "My menu description 1",
        },
    })


class MenuUpdate(MenuBase):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "My updated menu 1",
            "description": "My updated menu description 1",
        },
    })


class MenuOut(MenuBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    submenus_count: int
    dishes_count: int
