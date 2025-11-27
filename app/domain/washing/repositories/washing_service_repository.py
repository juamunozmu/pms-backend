from abc import ABC, abstractmethod
from typing import List
from datetime import date

class WashingServiceRepository(ABC):
    @abstractmethod
    async def get_total_income_by_shift(self, shift_id: int) -> int:
        """Calcula el ingreso total de lavados para un turno."""
        pass

    @abstractmethod
    async def get_total_sales_by_washer_and_date(self, washer_id: int, date: str) -> int:
        """Calcula el total de ventas de un lavador en una fecha específica."""
        pass

    @abstractmethod
    async def get_washing_duration_stats(self, start_date: date, end_date: date) -> List[dict]:
        """Obtiene estadísticas de duración de lavados agrupadas por lavador y tipo de servicio."""
        pass
