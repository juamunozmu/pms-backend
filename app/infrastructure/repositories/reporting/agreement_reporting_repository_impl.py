from typing import List
from datetime import date, datetime, time
from sqlalchemy import select, func, and_
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.subscriptions import Agreement, AgreementVehicle
from app.infrastructure.database.models.vehicles import Vehicle
from app.infrastructure.database.models.services import WashingService
from app.domain.reporting.repositories.agreement_reporting_repository import IAgreementReportingRepository
from app.application.dto.reporting.agreement_report_response import AgreementReportItem

class AgreementReportingRepositoryImpl(IAgreementReportingRepository):
    async def get_agreement_stats(self, start_date: date, end_date: date) -> List[AgreementReportItem]:
        async with SessionLocal() as session:
            # Convert dates to datetime for comparison
            start_dt = datetime.combine(start_date, time.min)
            end_dt = datetime.combine(end_date, time.max)

            stmt = (
                select(
                    Agreement.company_name,
                    func.count(WashingService.id).label("total_washes"),
                    func.sum(WashingService.price).label("total_amount")
                )
                .join(AgreementVehicle, Agreement.id == AgreementVehicle.agreement_id)
                .join(Vehicle, AgreementVehicle.vehicle_id == Vehicle.id)
                .join(WashingService, Vehicle.id == WashingService.vehicle_id)
                .where(
                    and_(
                        WashingService.service_date >= start_dt,
                        WashingService.service_date <= end_dt,
                        WashingService.payment_status != 'cancelled'
                    )
                )
                .group_by(Agreement.company_name)
            )

            result = await session.execute(stmt)
            rows = result.all()

            return [
                AgreementReportItem(
                    company_name=row.company_name,
                    total_washes=row.total_washes,
                    total_amount=row.total_amount or 0
                )
                for row in rows
            ]
