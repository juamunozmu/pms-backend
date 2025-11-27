from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class ShiftCreate(BaseModel):
    initial_cash: int

class ShiftResponse(BaseModel):
    id: int
    admin_id: int
    shift_date: date
    start_time: datetime
    end_time: Optional[datetime]
    initial_cash: int
    final_cash: Optional[int]
    total_income: int
    total_expenses: int
    notes: Optional[str]

    class Config:
        from_attributes = True
