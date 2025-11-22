from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.washers.entities.washer import Washer


class IWasherRepository(ABC):

    @abstractmethod
    async def create(self, washer: Washer) -> Washer:
        pass

    @abstractmethod
    async def list(self) -> List[Washer]:
        pass

    @abstractmethod
    async def get(self, washer_id: int) -> Optional[Washer]:
        pass

    @abstractmethod
    async def update(self, washer_id: int, washer: Washer) -> Washer:
        pass

    @abstractmethod
    async def delete(self, washer_id: int):
        pass
