from datetime import datetime, timezone
from typing import Optional
from app.domain.parking.entities.parking_record import ParkingRecord
from app.domain.parking.repositories.vehicle_repository import IVehicleRepository
from app.domain.parking.repositories.parking_record_repository import IParkingRecordRepository
from app.domain.parking.repositories.rate_repository import IRateRepository


class VehicleExitUseCase:
    """Use case for registering vehicle exit from parking"""
    
    def __init__(
        self,
        vehicle_repo: IVehicleRepository,
        parking_record_repo: IParkingRecordRepository,
        rate_repo: IRateRepository
    ):
        self.vehicle_repo = vehicle_repo
        self.parking_record_repo = parking_record_repo
        self.rate_repo = rate_repo
    
    async def execute(
        self,
        plate: str,
        notes: Optional[str] = None
    ) -> ParkingRecord:
        """
        Register a vehicle exit from the parking lot and calculate the total cost.
        
        Args:
            plate: Vehicle license plate
            notes: Optional notes for the exit
            
        Returns:
            Updated ParkingRecord with exit time and total cost
            
        Raises:
            ValueError: If vehicle not found or no active parking record
        """
        # Normalize plate to uppercase
        plate = plate.upper().strip()
        
        # Find vehicle
        vehicle = await self.vehicle_repo.get_by_plate(plate)
        if not vehicle:
            raise ValueError(f"Vehicle with plate {plate} not found")
        
        # Find active parking record
        parking_record = await self.parking_record_repo.get_active_by_vehicle_id(vehicle.id)
        if not parking_record:
            raise ValueError(f"No active parking record found for vehicle {plate}")
        
        # Set exit time
        exit_time = datetime.now(timezone.utc)
        parking_record.exit_time = exit_time
        
        # Calculate parking duration in hours (rounded up)
        duration = exit_time - parking_record.entry_time
        hours = duration.total_seconds() / 3600
        
        # Round up to nearest hour (minimum 1 hour)
        import math
        hours_rounded = max(1, math.ceil(hours))
        
        # Get the rate
        rate = await self.rate_repo.get_by_id(parking_record.parking_rate_id)
        if not rate:
            raise ValueError(f"Rate not found for parking record")
        
        # Calculate parking cost (rate.price is per hour in centavos)
        parking_cost = rate.price * hours_rounded
        
        # Calculate total cost (parking + helmet charge)
        total_cost = parking_cost + parking_record.helmet_charge
        
        parking_record.total_cost = total_cost
        parking_record.payment_status = "paid"  # Assuming immediate payment
        
        if notes:
            parking_record.notes = notes
        
        # Update parking record
        updated_record = await self.parking_record_repo.update(
            parking_record.id,
            parking_record
        )
        
        return updated_record
