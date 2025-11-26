from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ExpenseCreate(BaseModel):
    expense_type: str
    amount: int
    description: str
    expense_date: date
    shift_id: Optional[int] = None

class ExpenseResponse(BaseModel):
    id: int
    expense_type: str
    amount: int
    description: str
    expense_date: date
    shift_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
