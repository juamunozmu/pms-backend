from datetime import date
import csv
import io
from app.domain.reporting.repositories.agreement_reporting_repository import IAgreementReportingRepository
from app.application.dto.reporting.agreement_report_response import AgreementReportResponse

class AgreementReportingService:
    def __init__(self, repo: IAgreementReportingRepository):
        self.repo = repo

    async def get_report(self, start_date: date, end_date: date) -> AgreementReportResponse:
        items = await self.repo.get_agreement_stats(start_date, end_date)
        return AgreementReportResponse(
            start_date=start_date,
            end_date=end_date,
            items=items
        )

    async def generate_csv(self, start_date: date, end_date: date) -> str:
        report = await self.get_report(start_date, end_date)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["Company Name", "Total Washes", "Total Amount (COP)"])
        
        # Rows
        for item in report.items:
            writer.writerow([
                item.company_name, 
                item.total_washes, 
                item.total_amount / 100.0 # Convert cents to units
            ])
            
        return output.getvalue()
