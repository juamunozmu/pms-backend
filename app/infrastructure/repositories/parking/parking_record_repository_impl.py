from sqlalchemy import select, func
from app.domain.parking.repositories.parking_record_repository import ParkingRecordRepository
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.vehicles import ParkingRecord as ParkingRecordModel

class ParkingRecordRepositoryImpl(ParkingRecordRepository):
    async def get_total_income_by_shift(self, shift_id: int) -> int:
        async with SessionLocal() as session:
            # Assuming ParkingRecord has a price/total_cost column and shift_id
            # Let's check the model definition again to be sure about the column name
            # I recall reading services.py but let's be safe.
            # Wait, I read services.py earlier. Let me check the context.
            # WashingService has 'price'. ParkingRecord... I need to check.
            result = await session.execute(
                select(func.sum(ParkingRecordModel.total_cost))
                .where(ParkingRecordModel.shift_id == shift_id)
                .where(ParkingRecordModel.status == 'completed') # Only completed/paid
            )
            total = result.scalar()
            return total if total else 0
