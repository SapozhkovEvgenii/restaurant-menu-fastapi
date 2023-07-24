import uuid

from sqlalchemy import Column, ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import UUID


from app.core.db import Base


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    title = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)

    price = Column(String, nullable=False)
    parent_id = Column(String, ForeignKey("submenu.id"))
