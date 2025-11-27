from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.financial.entities.employee_advance import EmployeeAdvance

class EmployeeAdvanceRepository(ABC):
    @abstractmethod
    async def save(self, advance: EmployeeAdvance) -> EmployeeAdvance:
        """Guarda un vale (crear o actualizar)."""
        pass

    @abstractmethod
    async def get_by_id(self, advance_id: int) -> Optional[EmployeeAdvance]:
        """Obtiene un vale por su ID."""
        pass

    @abstractmethod
    async def get_active_by_washer(self, washer_id: int) -> List[EmployeeAdvance]:
        """Obtiene los vales activos de un lavador."""
        pass
