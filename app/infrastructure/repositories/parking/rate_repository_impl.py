from typing import Optional, List
from sqlalchemy import select
from app.domain.parking.entities.rate import Rate
from app.domain.parking.repositories.rate_repository import IRateRepository
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.services import Rate as RateModel

class RateRepositoryImpl(IRateRepository):
    
    def _to_entity(self, model: RateModel) -> Optional[Rate]:
        if not model:
            return None
        return Rate(
            id=model.id,
            vehicle_type=model.vehicle_type,
            rate_type=model.rate_type,
            price=model.price,
            description=model.description,
            is_active=model.is_active
        )

    async def get_active_by_type(self, vehicle_type: str, rate_type: str) -> Optional[Rate]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(RateModel)
                .where(RateModel.vehicle_type == vehicle_type)
                .where(RateModel.rate_type == rate_type)
                .where(RateModel.is_active == True)
            )
            model = result.scalar_one_or_none()
            return self._to_entity(model)

    async def get_by_id(self, rate_id: int) -> Optional[Rate]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(RateModel).where(RateModel.id == rate_id)
            )
            model = result.scalar_one_or_none()
            return self._to_entity(model)

    async def list_active(self) -> List[Rate]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(RateModel).where(RateModel.is_active == True)
            )
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]
