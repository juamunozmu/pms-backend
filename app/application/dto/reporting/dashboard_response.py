from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class GeneralMetrics(BaseModel):
    total_income: int
    total_expenses: int
    total_bonuses: int
    net_performance: int
    avg_daily_income: int
    avg_daily_expenses: int
    income_vs_expenses_ratio: float  # Income / Expenses (handle div by zero)

class OperationalMetrics(BaseModel):
    avg_occupancy_level: float  # Average number of cars parked
    avg_washing_time_minutes: float
    personnel_utilization_percentage: float

class TrendPoint(BaseModel):
    date: date
    income: int
    expenses: int
    bonuses: int

class DashboardMetricsResponse(BaseModel):
    start_date: date
    end_date: date
    general: GeneralMetrics
    operational: OperationalMetrics
    trends: List[TrendPoint]
