from typing import List, Optional
from datetime import date
from sqlalchemy import select, extract, func
from app.domain.financial.repositories.bonus_repository import BonusRepository
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.financial import Bonus

class BonusRepositoryImpl(BonusRepository):
    async def create(self, bonus: Bonus) -> Bonus:
        async with SessionLocal() as session:
            session.add(bonus)
            await session.commit()
            await session.refresh(bonus)
            return bonus

    async def get_by_washer_and_date(self, washer_id: int, bonus_date: date) -> Optional[Bonus]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(Bonus)
                .where(Bonus.washer_id == washer_id)
                .where(Bonus.bonus_date == bonus_date)
            )
            return result.scalar_one_or_none()

    async def get_by_date(self, bonus_date: date) -> List[Bonus]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(Bonus)
                .where(Bonus.bonus_date == bonus_date)
            )
            return result.scalars().all()

    async def get_monthly_summary(self, month: int, year: int) -> List[dict]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(
                    Bonus.washer_id,
                    func.sum(Bonus.amount).label("total_amount")
                )
                .where(extract('month', Bonus.bonus_date) == month)
                .where(extract('year', Bonus.bonus_date) == year)
                .group_by(Bonus.washer_id)
            )
            
            return [{"washer_id": row.washer_id, "total_amount": row.total_amount} for row in result]
