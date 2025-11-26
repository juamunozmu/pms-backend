from pydantic import BaseModel, EmailStr
from typing import Optional

class WasherResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    commission_percentage: int
    is_active: bool

    class Config:
        from_attributes = True