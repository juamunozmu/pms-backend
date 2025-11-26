from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class WasherCreateRequest(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    commission_percentage: int = Field(..., ge=0, le=100)
    password: str = Field(..., min_length=6)  # Needed for creation

class WasherUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    commission_percentage: Optional[int] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None