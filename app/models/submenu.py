import uuid

from sqlalchemy import Column, ForeignKey, String, Text, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship

from app.core.db import Base
from app.models.dish import Dish


class SubMenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    title = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('menu.id'))
    dishes = relationship('Dish', cascade='delete',
                          backref='submenu', lazy='selectin')
    dishes_count = column_property(
        select(func.count(Dish.id)).where(
            Dish.parent_id == id).scalar_subquery(),
    )
