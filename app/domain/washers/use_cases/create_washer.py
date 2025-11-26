from app.domain.washers.repositories.washer_repository import IWasherRepository
from app.domain.washers.entities.washer import Washer
from app.application.dto.washers.washer_request import WasherCreateRequest


class CreateWasher:

    def __init__(self, repo: IWasherRepository):
        self.repo = repo

    async def execute(self, data: WasherCreateRequest):
        # TODO: Implement proper password hashing
        password_hash = f"hashed_{data.password}"
        
        washer = Washer(
            id=None,
            full_name=data.full_name,
            email=data.email,
            phone=data.phone,
            commission_percentage=data.commission_percentage,
            is_active=True,
            password_hash=password_hash
        )
        return await self.repo.create(washer)
