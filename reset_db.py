import asyncio
import sys
import os

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

# Fix for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.infrastructure.database.session import engine
from app.infrastructure.database.models import Base

async def main():
    print("Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        # Also drop alembic_version table if it exists (drop_all might not catch it if it's not in metadata)
        from sqlalchemy import text
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
    print("All tables dropped.")

if __name__ == "__main__":
    asyncio.run(main())
