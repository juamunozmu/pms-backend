from typing import List
from datetime import datetime
from sqlalchemy import select, or_, and_
from app.infrastructure.database.session import SessionLocal
from app.infrastructure.database.models.vehicles import ParkingRecord
from app.domain.reporting.repositories.occupancy_reporting_repository import OccupancyReportingRepository

class OccupancyReportingRepositoryImpl(OccupancyReportingRepository):
    async def get_parking_records_overlapping(self, start_time: datetime, end_time: datetime) -> List[ParkingRecord]:
        async with SessionLocal() as session:
            # Buscamos registros donde:
            # La entrada fue antes del fin del rango Y (la salida fue después del inicio del rango O aún no ha salido)
            stmt = select(ParkingRecord).where(
                and_(
                    ParkingRecord.entry_time <= end_time,
                    or_(
                        ParkingRecord.exit_time == None,
                        ParkingRecord.exit_time >= start_time
                    )
                )
            )
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_total_parking_duration_seconds(self, start_time: datetime, end_time: datetime) -> float:
        # Implementación en memoria por ahora (reutilizando la query anterior)
        # Para producción con millones de registros, esto debería ser una query SQL nativa compleja.
        records = await self.get_parking_records_overlapping(start_time, end_time)
        total_seconds = 0.0
        
        # Asegurar que start_time y end_time tengan zona horaria si los registros la tienen
        # Asumimos que vienen con TZ correcta o ambas naive.
        
        for record in records:
            # Definir inicio y fin efectivos del registro dentro de la ventana
            # entry_time y exit_time son TIMESTAMP(timezone=True) -> datetime aware
            
            rec_entry = record.entry_time
            rec_exit = record.exit_time
            
            # Normalizar zonas horarias si es necesario (simple check)
            # Si rec_entry es aware y start_time es naive, hacemos start_time aware (con la tz de rec_entry)
            # O hacemos rec_entry naive. Preferible hacer todo naive para cálculo simple si asumimos misma zona.
            
            if rec_entry.tzinfo is not None and start_time.tzinfo is None:
                # Opción A: Asignar tz a start_time. Pero start_time es constante.
                # Opción B: Quitar tz a rec_entry.
                rec_entry = rec_entry.replace(tzinfo=None)
            
            if rec_exit and rec_exit.tzinfo is not None and end_time.tzinfo is None:
                rec_exit = rec_exit.replace(tzinfo=None)
                
            effective_start = max(rec_entry, start_time)
            
            effective_end = end_time
            if rec_exit:
                effective_end = min(rec_exit, end_time)
            
            # Si el carro sigue parqueado (exit=None), su duración cuenta hasta el final del reporte (end_time)
            # o hasta "ahora" si end_time es futuro? 
            # Asumimos end_time es el corte del reporte.
            
            if effective_end > effective_start:
                total_seconds += (effective_end - effective_start).total_seconds()
                
        return total_seconds
