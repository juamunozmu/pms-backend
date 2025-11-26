from abc import ABC, abstractmethod
from typing import Optional
from app.domain.users.entities.global_admin import GlobalAdmin

class IGlobalAdminRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[GlobalAdmin]:
        pass

    @abstractmethod
    async def get_by_id(self, admin_id: int) -> Optional[GlobalAdmin]:
        pass
    
    @abstractmethod
    async def update_last_login(self, admin_id: int) -> None:
        pass

    @abstractmethod
    async def update_password(self, admin_id: int, new_password_hash: str) -> None:
        pass
