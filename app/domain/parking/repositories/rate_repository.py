from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.parking.entities.rate import Rate

class IRateRepository(ABC):
    @abstractmethod
    async def get_active_by_type(self, vehicle_type: str, rate_type: str) -> Optional[Rate]:
        pass

    @abstractmethod
    async def get_by_id(self, rate_id: int) -> Optional[Rate]:
        pass

    @abstractmethod
    async def list_active(self) -> List[Rate]:
        pass
