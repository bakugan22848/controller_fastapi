from typing import List

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import Base


class BaseRepository:
    model : Base = None

    def __init__(self, session : AsyncSession):
        self.session = session

    async def create_one(self, data: dict) -> model:
        row = self.model(**data)
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def get_many(self) -> List[model]:
        query = select(self.model)
        result = await self.session.execute(query)
        rows = result.scalars().all()
        return rows

    async def get_many_by(self, **params) -> List[model]:
        query = select(self.model).filter_by(**params)
        result = await self.session.execute(query)
        rows = result.scalars().all()
        return rows

    async def get_one(self, **params) -> model:
        query = select(self.model).filter_by(**params)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return row

    async def update_one(self, data: dict, **params) -> model:
        query = update(self.model).filter_by(**params).values(**data).returning(self.model)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        await self.session.refresh(row)
        return row

    async def delete_one(self, **params) -> model:
        query = delete(self.model).filter_by(**params).returning(self.model)
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()
        return row
