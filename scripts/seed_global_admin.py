import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.users import GlobalAdmin
from app.core.security import get_password_hash
from sqlalchemy import select

async def seed_admin():
    async with SessionLocal() as session:
        # Check if exists
        result = await session.execute(select(GlobalAdmin).where(GlobalAdmin.email == "admin@pms.com"))
        admin = result.scalar_one_or_none()
        if admin:
            print("Admin already exists. Updating password...")
            admin.password_hash = get_password_hash("admin123")
            session.add(admin)
            await session.commit()
            print("Global Admin password updated: admin@pms.com / admin123")
            return

        admin = GlobalAdmin(
            email="admin@pms.com",
            full_name="Super Admin",
            password_hash=get_password_hash("admin123"),
            is_active=True
        )
        session.add(admin)
        await session.commit()
        print("Global Admin created: admin@pms.com / admin123")

if __name__ == "__main__":
    asyncio.run(seed_admin())
