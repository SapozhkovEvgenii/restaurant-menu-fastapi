import uuid

from pydantic import BaseModel, ConfigDict, field_validator


class DishBase(BaseModel):
    title: str
    description: str
    price: str

    @field_validator('price')
    def check_price(cls, value: str):
        if not float(value):
            raise ValueError('price must be a number')
        value = format(float(value), '.2f')
        return value


class DishCreate(DishBase):
    model_config = ConfigDict(json_schema_extra={
        'example': {
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50',
        },
    })


class DishUpdate(DishCreate):
    model_config = ConfigDict(json_schema_extra={
        'example': {
            'title': 'My updated dish 1',
            'description': 'My updated dish description 1',
            'price': '14.50',
        },
    })


class DishOut(DishBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
