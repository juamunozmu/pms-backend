import asyncio
import sys
import os

# Add the parent directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from app.infrastructure.database.session import SessionLocal
from app.domain.reporting.services.revenue_service import RevenueService

async def main():
    print("Connecting to database...")
    async with SessionLocal() as db:
        print("Initializing RevenueService...")
        service = RevenueService(db)
        print("Fetching consolidated revenue...")
        try:
            report = await service.get_consolidated_revenue(
                start_date=date(2025, 1, 1),
                end_date=date(2025, 12, 31),
                group_by='month'
            )
            print("Report generated successfully:")
            print(report.model_dump_json(indent=2))
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
