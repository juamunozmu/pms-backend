from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class RevenueStats(BaseModel):
    date: date
    parking_income: int = 0
    washing_income: int = 0
    subscription_income: int = 0
    total_income: int = 0

class RevenueReportResponse(BaseModel):
    start_date: date
    end_date: date
    group_by: str
    data: List[RevenueStats]
    total_period_income: int
