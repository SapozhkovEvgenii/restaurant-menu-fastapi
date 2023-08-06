import uuid

from sqlalchemy import Column, String, Text, and_, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship

from app.core.db import Base
from app.models.dish import Dish
from app.models.submenu import SubMenu


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    title = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    submenus = relationship(
        'SubMenu', cascade='delete', backref='menu', lazy='selectin'
    )
    submenus_count = column_property(
        select(func.count(SubMenu.id)).where(SubMenu.parent_id == id).scalar_subquery(),
    )
    dishes_count: int = column_property(
        select(func.count(Dish.id))
        .join(SubMenu)
        .where(and_(SubMenu.parent_id == id, SubMenu.id == Dish.parent_id))
        .correlate_except(Dish)
        .scalar_subquery()
    )
