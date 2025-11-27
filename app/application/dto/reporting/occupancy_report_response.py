from pydantic import BaseModel
from typing import List
from datetime import date

class OccupancyDataPoint(BaseModel):
    hour: str  # "08:00", "09:00"
    count: int

class OccupancyReportResponse(BaseModel):
    report_date: date
    items: List[OccupancyDataPoint]
    total_peak_occupancy: int
    peak_hour: str
