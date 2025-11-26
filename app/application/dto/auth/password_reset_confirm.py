from pydantic import BaseModel

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
