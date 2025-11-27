from typing import List, Optional
from sqlalchemy import select, and_
from app.domain.financial.entities.employee_advance import EmployeeAdvance
from app.domain.financial.repositories.employee_advance_repository import EmployeeAdvanceRepository
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.financial import EmployeeAdvance as EmployeeAdvanceModel

class EmployeeAdvanceRepositoryImpl(EmployeeAdvanceRepository):

    def _to_entity(self, model: EmployeeAdvanceModel) -> Optional[EmployeeAdvance]:
        if not model:
            return None
        return EmployeeAdvance(
            id=model.id,
            washer_id=model.washer_id,
            total_amount=model.total_amount,
            number_of_installments=model.number_of_installments,
            installment_amount=model.installment_amount,
            remaining_amount=model.remaining_amount,
            status=model.status,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def save(self, advance: EmployeeAdvance) -> EmployeeAdvance:
        async with SessionLocal() as session:
            if advance.id:
                # Update
                result = await session.execute(
                    select(EmployeeAdvanceModel).where(EmployeeAdvanceModel.id == advance.id)
                )
                model = result.scalar_one_or_none()
                if model:
                    model.remaining_amount = advance.remaining_amount
                    model.status = advance.status
                    await session.commit()
                    await session.refresh(model)
                    return self._to_entity(model)
            
            # Create
            model = EmployeeAdvanceModel(
                washer_id=advance.washer_id,
                total_amount=advance.total_amount,
                number_of_installments=advance.number_of_installments,
                installment_amount=advance.installment_amount,
                remaining_amount=advance.remaining_amount,
                status=advance.status,
                description=advance.description
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)

    async def get_by_id(self, advance_id: int) -> Optional[EmployeeAdvance]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(EmployeeAdvanceModel).where(EmployeeAdvanceModel.id == advance_id)
            )
            model = result.scalar_one_or_none()
            return self._to_entity(model)

    async def get_active_by_washer(self, washer_id: int) -> List[EmployeeAdvance]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(EmployeeAdvanceModel).where(
                    and_(
                        EmployeeAdvanceModel.washer_id == washer_id,
                        EmployeeAdvanceModel.status == 'active'
                    )
                )
            )
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]
