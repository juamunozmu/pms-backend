from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Expense:
    expense_type: str
    amount: int  # In cents
    description: str
    expense_date: date
    id: Optional[int] = None
    shift_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
