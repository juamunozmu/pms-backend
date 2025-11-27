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
        # Instead of relying on metadata.drop_all which can fail with constraint mismatches,
        # we will drop the entire public schema and recreate it. This is a nuclear option
        # but effective for a full reset.
        from sqlalchemy import text
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
    print("All tables dropped (Schema public recreated).")

if __name__ == "__main__":
    asyncio.run(main())
