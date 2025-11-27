from abc import ABC, abstractmethod

class ParkingRecordRepository(ABC):
    @abstractmethod
    async def get_total_income_by_shift(self, shift_id: int) -> int:
        """Calcula el ingreso total de parqueo para un turno."""
        pass
