import uuid

from pydantic import BaseModel, ConfigDict


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    model_config = ConfigDict(json_schema_extra={
        'example': {
            'title': 'My submenu 1',
            'description': 'My submenu description 1',
        },
    })


class SubMenuUpdate(SubMenuBase):
    model_config = ConfigDict(json_schema_extra={
        'example': {
            'title': 'My updated submenu 1',
            'description': 'My updated submenu description 1',
        },
    })


class SubMenuOut(SubMenuBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    dishes_count: int
