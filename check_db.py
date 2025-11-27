import asyncio
import sys
import os

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

# Fix for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.infrastructure.database.session import engine
from sqlalchemy import inspect, text

async def main():
    try:
        async with engine.connect() as conn:
            def get_tables(sync_conn):
                return inspect(sync_conn).get_table_names()
            
            tables = await conn.run_sync(get_tables)
            print(f"Tables: {tables}")
            
            try:
                result = await conn.execute(text("SELECT * FROM alembic_version"))
                print(f"Alembic version: {result.fetchall()}")
            except Exception as e:
                print(f"Could not read alembic_version: {e}")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
