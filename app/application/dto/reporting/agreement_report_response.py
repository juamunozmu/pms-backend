from pydantic import BaseModel
from typing import List
from datetime import date

class AgreementReportItem(BaseModel):
    company_name: str
    total_washes: int
    total_amount: int  # In cents

class AgreementReportResponse(BaseModel):
    start_date: date
    end_date: date
    items: List[AgreementReportItem]
