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

class PerformanceReportResponse(BaseModel):
    start_date: date
    end_date: date
    total_income: int
    total_expenses: int
    total_bonuses: int
    net_performance: int

class WashingDurationStat(BaseModel):
    washer_id: Optional[int]
    service_type: str
    avg_duration_minutes: float
    count: int

class WashingAnalyticsResponse(BaseModel):
    start_date: date
    end_date: date
    stats: List[WashingDurationStat]
