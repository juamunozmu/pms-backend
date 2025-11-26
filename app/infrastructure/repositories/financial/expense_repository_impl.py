from typing import List, Optional
from sqlalchemy import select, delete
from app.domain.financial.entities.expense import Expense
from app.domain.financial.repositories.expense_repository import ExpenseRepository
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.financial import Expense as ExpenseModel

class ExpenseRepositoryImpl(ExpenseRepository):

    def _to_entity(self, model: ExpenseModel) -> Optional[Expense]:
        if not model:
            return None
        return Expense(
            id=model.id,
            shift_id=model.shift_id,
            expense_type=model.expense_type,
            amount=model.amount,
            description=model.description,
            expense_date=model.expense_date,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def save(self, expense: Expense) -> Expense:
        async with SessionLocal() as session:
            # For now, we only handle creation as per HUs. 
            # If ID exists, we would update, but let's keep it simple for now.
            model = ExpenseModel(
                shift_id=expense.shift_id,
                expense_type=expense.expense_type,
                amount=expense.amount,
                description=expense.description,
                expense_date=expense.expense_date
            )
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._to_entity(model)

    async def get_by_id(self, expense_id: int) -> Optional[Expense]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(ExpenseModel).where(ExpenseModel.id == expense_id)
            )
            model = result.scalar_one_or_none()
            return self._to_entity(model)

    async def delete(self, expense_id: int) -> None:
        async with SessionLocal() as session:
            await session.execute(
                delete(ExpenseModel).where(ExpenseModel.id == expense_id)
            )
            await session.commit()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Expense]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(ExpenseModel).offset(skip).limit(limit)
            )
            models = result.scalars().all()
            return [self._to_entity(m) for m in models]
