from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class EmployeeAdvance:
    washer_id: int
    total_amount: int
    number_of_installments: int
    installment_amount: int
    remaining_amount: int
    description: str
    id: Optional[int] = None
    status: str = "active"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
