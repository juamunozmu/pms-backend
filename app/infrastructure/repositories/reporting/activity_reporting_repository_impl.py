from typing import List
from datetime import date, datetime, time
from sqlalchemy import select, func, and_
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.services import WashingService
from app.domain.reporting.repositories.activity_reporting_repository import IActivityReportingRepository
from app.application.dto.reporting.activity_report_response import ActivityReportItem

class ActivityReportingRepositoryImpl(IActivityReportingRepository):
    async def get_daily_activity(self, start_date: date, end_date: date) -> List[ActivityReportItem]:
        async with SessionLocal() as session:
            start_dt = datetime.combine(start_date, time.min)
            end_dt = datetime.combine(end_date, time.max)

            # Group by date (using func.date for PostgreSQL/SQLite compatibility usually requires care, 
            # but here we will fetch raw data or group by day if possible. 
            # To be safe and DB-agnostic, we can group by the date part of the timestamp)
            
            # For simplicity and robustness across DBs (SQLite vs Postgres date functions differ),
            # we will fetch grouped by date using SQLAlchemy's generic func.date if possible,
            # or just cast to date.
            
            # Using func.date(WashingService.service_date) works in SQLite and Postgres
            stmt = (
                select(
                    func.date(WashingService.service_date).label("service_day"),
                    func.count(WashingService.id).label("count"),
                    func.sum(WashingService.price).label("total_amount")
                )
                .where(
                    and_(
                        WashingService.service_date >= start_dt,
                        WashingService.service_date <= end_dt,
                        WashingService.payment_status != 'cancelled'
                    )
                )
                .group_by(func.date(WashingService.service_date))
                .order_by(func.date(WashingService.service_date))
            )

            result = await session.execute(stmt)
            rows = result.all()

            return [
                ActivityReportItem(
                    label=str(row.service_day),
                    count=row.count,
                    total_amount=row.total_amount or 0
                )
                for row in rows
            ]
