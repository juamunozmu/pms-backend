from dataclasses import dataclass

@dataclass
class Washer:
    id: int | None
    full_name: str
    email: str
    phone: str | None
    commission_percentage: int
    is_active: bool = True
    password_hash: str | None = None