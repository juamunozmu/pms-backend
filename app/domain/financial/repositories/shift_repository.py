from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.financial.entities.shift import Shift

class ShiftRepository(ABC):
    @abstractmethod
    async def save(self, shift: Shift) -> Shift:
        """Guarda un turno (crear o actualizar)."""
        pass

    @abstractmethod
    async def get_by_id(self, shift_id: int) -> Optional[Shift]:
        """Obtiene un turno por su ID."""
        pass
    
    @abstractmethod
    async def get_active_shift_by_admin(self, admin_id: int) -> Optional[Shift]:
        """Obtiene el turno activo actual de un administrador."""
        pass

    @abstractmethod
    async def get_by_date_and_admin(self, date_val, admin_id: int) -> Optional[Shift]:
        """Obtiene un turno por fecha y administrador."""
        pass
