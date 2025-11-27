from datetime import date, datetime
from typing import List, Dict
from collections import defaultdict
from app.domain.reporting.repositories.activity_reporting_repository import IActivityReportingRepository
from app.application.dto.reporting.activity_report_response import ActivityReportResponse, ActivityReportItem

class ActivityReportingService:
    def __init__(self, repo: IActivityReportingRepository):
        self.repo = repo

    async def get_activity_report(self, start_date: date, end_date: date, group_by: str = "day") -> ActivityReportResponse:
        # 1. Get daily data from DB
        daily_items = await self.repo.get_daily_activity(start_date, end_date)
        
        # 2. Process grouping in Python (DB agnostic and easier for week/month logic)
        grouped_items: List[ActivityReportItem] = []
        
        if group_by == "day":
            grouped_items = daily_items
            
        elif group_by == "week":
            temp_map: Dict[str, ActivityReportItem] = defaultdict(lambda: ActivityReportItem(label="", count=0, total_amount=0))
            
            for item in daily_items:
                # Parse date string back to date object
                dt = datetime.strptime(item.label, "%Y-%m-%d").date()
                # Get ISO week number (e.g., "2023-W45")
                week_label = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
                
                entry = temp_map[week_label]
                entry.label = week_label
                entry.count += item.count
                entry.total_amount += item.total_amount
            
            grouped_items = sorted(list(temp_map.values()), key=lambda x: x.label)
            
        elif group_by == "month":
            temp_map: Dict[str, ActivityReportItem] = defaultdict(lambda: ActivityReportItem(label="", count=0, total_amount=0))
            
            for item in daily_items:
                dt = datetime.strptime(item.label, "%Y-%m-%d").date()
                # Month format (e.g., "2023-11")
                month_label = f"{dt.year}-{dt.month:02d}"
                
                entry = temp_map[month_label]
                entry.label = month_label
                entry.count += item.count
                entry.total_amount += item.total_amount
                
            grouped_items = sorted(list(temp_map.values()), key=lambda x: x.label)

        return ActivityReportResponse(
            start_date=start_date,
            end_date=end_date,
            group_by=group_by,
            items=grouped_items
        )
