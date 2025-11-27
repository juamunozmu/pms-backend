from pydantic import BaseModel
from typing import List
from datetime import date

class ActivityReportItem(BaseModel):
    label: str  # Date or Week or Month
    count: int
    total_amount: int  # In cents

class ActivityReportResponse(BaseModel):
    start_date: date
    end_date: date
    group_by: str
    items: List[ActivityReportItem]
