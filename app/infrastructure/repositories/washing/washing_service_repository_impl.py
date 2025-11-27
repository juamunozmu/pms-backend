from sqlalchemy import select, func, cast, Date
from datetime import date
from typing import List
from app.domain.washing.repositories.washing_service_repository import WashingServiceRepository
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.services import WashingService as WashingServiceModel

class WashingServiceRepositoryImpl(WashingServiceRepository):
    async def get_total_income_by_shift(self, shift_id: int) -> int:
        async with SessionLocal() as session:
            result = await session.execute(
                select(func.sum(WashingServiceModel.price))
                .where(WashingServiceModel.shift_id == shift_id)
                .where(WashingServiceModel.payment_status == 'paid') # Only count paid services? Or all? Usually paid.
            )
            total = result.scalar()
            return total if total else 0

    async def get_total_sales_by_washer_and_date(self, washer_id: int, date: str) -> int:
        async with SessionLocal() as session:
            # Convert string date to date object if necessary, or rely on SQLAlchemy to handle it
            # Assuming date is passed as a date object or string in 'YYYY-MM-DD' format
            
            # We need to filter by washer_id and the date part of created_at or a specific date column
            # WashingService has created_at (TIMESTAMP). We should cast it to date.
            
            result = await session.execute(
                select(func.sum(WashingServiceModel.price))
                .where(WashingServiceModel.washer_id == washer_id)
                .where(func.date(WashingServiceModel.created_at) == date)
                .where(WashingServiceModel.payment_status == 'paid')
            )
            total = result.scalar()
            return total if total else 0

    async def get_washing_duration_stats(self, start_date: date, end_date: date) -> List[dict]:
        async with SessionLocal() as session:
            stmt = (
                select(
                    WashingServiceModel.washer_id,
                    WashingServiceModel.service_type,
                    func.avg(WashingServiceModel.end_time - WashingServiceModel.start_time).label("avg_duration"),
                    func.count(WashingServiceModel.id).label("count")
                )
                .where(cast(WashingServiceModel.service_date, Date) >= start_date)
                .where(cast(WashingServiceModel.service_date, Date) <= end_date)
                .where(WashingServiceModel.start_time.isnot(None))
                .where(WashingServiceModel.end_time.isnot(None))
                .group_by(WashingServiceModel.washer_id, WashingServiceModel.service_type)
            )
            result = await session.execute(stmt)
            return [
                {
                    "washer_id": row.washer_id,
                    "service_type": row.service_type,
                    "avg_duration": row.avg_duration, # This will be a timedelta
                    "count": row.count
                }
                for row in result
            ]
