from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.domain.washers.entities.washer import Washer
from app.domain.washers.repositories.washer_repository import IWasherRepository
from app.infrastructure.database.session import get_session


class WasherRepositoryImpl(IWasherRepository):

    async def create(self, washer: Washer) -> Washer:
        async with get_session() as session:
            session.add(washer)
            await session.commit()
            await session.refresh(washer)
            return washer

    async def list(self) -> List[Washer]:
        async with get_session() as session:
            result = await session.execute(select(Washer))
            return result.scalars().all()

    async def get(self, washer_id: int) -> Optional[Washer]:
        async with get_session() as session:
            result = await session.execute(
                select(Washer).where(Washer.id == washer_id)
            )
            return result.scalar_one_or_none()

    async def update(self, washer_id: int, washer: Washer) -> Washer:
        async with get_session() as session:
            await session.execute(
                update(Washer)
                .where(Washer.id == washer_id)
                .values(
                    name=washer.name,
                    phone=washer.phone,
                    status=washer.status
                )
            )
            await session.commit()

            result = await session.execute(
                select(Washer).where(Washer.id == washer_id)
            )
            return result.scalar_one()

    async def delete(self, washer_id: int):
        async with get_session() as session:
            await session.execute(
                delete(Washer).where(Washer.id == washer_id)
            )
            await session.commit()
