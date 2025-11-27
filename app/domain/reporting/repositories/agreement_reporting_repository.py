from abc import ABC, abstractmethod
from datetime import date
from typing import List
from app.application.dto.reporting.agreement_report_response import AgreementReportItem

class IAgreementReportingRepository(ABC):
    @abstractmethod
    async def get_agreement_stats(self, start_date: date, end_date: date) -> List[AgreementReportItem]:
        pass
