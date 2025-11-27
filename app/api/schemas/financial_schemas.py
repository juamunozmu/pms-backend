from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EmployeeAdvanceCreate(BaseModel):
    washer_id: int
    amount: int
    installments: int
    description: str

class EmployeeAdvanceResponse(BaseModel):
    id: int
    washer_id: int
    total_amount: int
    number_of_installments: int
    installment_amount: int
    remaining_amount: int
    status: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

class BonusCalculationResult(BaseModel):
    washer_id: int
    washer_name: str
    status: str
    total_sales: Optional[int] = 0
    gross_bonus: Optional[int] = 0
    deduction: Optional[int] = 0
    net_bonus: Optional[int] = 0
    reason: Optional[str] = None

class MonthlyBonusResponse(BaseModel):
    washer_id: int
    washer_name: str
    month: int
    year: int
    total_bonus: int
