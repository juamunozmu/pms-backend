from abc import ABC, abstractmethod

class IEmailService(ABC):
    @abstractmethod
    async def send_password_recovery_email(self, to_email: str, token: str) -> None:
        pass
