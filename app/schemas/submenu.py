from pydantic import BaseModel


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    menu_id = str

    class Config:
        schema_extra = {
            "example": {
                "title": "My submenu 1",
                "description": "My submenu description 1",
            },
        }


class SubMenuUpdate(SubMenuBase):
    class Config:
        schema_extra = {
            "example": {
                "title": "My updated submenu 1",
                "description": "My updated submenu description 1",
            },
        }


class SubMenuOut(SubMenuBase):
    id: str
    dishes_count: int

    class Config:
        orm_mode = True
