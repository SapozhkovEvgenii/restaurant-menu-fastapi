import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dish, Menu, SubMenu


class BaseRepository:
    """The repository contains the main methods of model instances"""

    def __init__(self, model: Menu | SubMenu | Dish):
        self.model = model

    async def get_instance(
            self,
            instance_id: uuid.UUID,
            session: AsyncSession):
        """Get one instance of model from the database by id."""

        instance = await session.execute(
            select(self.model).where(
                self.model.id == instance_id,
            ),
        )
        return instance.scalars().first()

    async def get_all_instances(self, session: AsyncSession):
        """Get all instances of model from the database."""

        all_instances = await session.execute(select(self.model))
        return all_instances.scalars().all()

    async def create_instance(self, input_data, session: AsyncSession):
        """Create an instance of model."""

        instance_data = input_data.dict()
        db_instance = self.model(**instance_data)
        session.add(db_instance)
        await session.commit()
        await session.refresh(db_instance)
        return db_instance

    async def update_instance(
            self,
            db_instance,
            input_data,
            session: AsyncSession):
        """Update the instance of model"""

        instance_data = jsonable_encoder(db_instance)
        update_data = input_data.model_dump(exclude_unset=True)

        for field in instance_data:
            if field in update_data:
                setattr(db_instance, field, update_data[field])
        session.add(db_instance)
        await session.commit()
        await session.refresh(db_instance)
        return db_instance

    async def delete_instance(self, db_instance, session: AsyncSession):
        """Delete the instance of model"""

        await session.delete(db_instance)
        await session.commit()
        return db_instance

    async def get_all_subobjects(
            self,
            object_id: uuid.UUID,
            session: AsyncSession):
        """Get all subobjects of the instance of model"""

        subobjects = await session.execute(
            select(self.model).where(self.model.parent_id == object_id))
        return subobjects.scalars().all()

    async def create_subobject(
        self,
        object_id: uuid.UUID,
        input_data,
        session: AsyncSession,
    ):
        instance_data = input_data.dict()
        db_subinstance = self.model(**instance_data, parent_id=object_id)
        session.add(db_subinstance)
        await session.commit()
        await session.refresh(db_subinstance)
        return db_subinstance
