import aiosmtplib
from email.message import EmailMessage
from app.core.config import settings
from app.domain.shared.interfaces.email_service import IEmailService

class SmtpEmailService(IEmailService):
    async def send_password_recovery_email(self, to_email: str, token: str) -> None:
        # In a real scenario, we would construct a proper HTML email
        # For now, we'll print to console if SMTP is not configured, or try to send if it is.
        
        subject = "Password Recovery - PMS"
        body = f"""
        Hello,
        
        You have requested to reset your password.
        Please use the following token to reset your password:
        
        {token}
        
        This token will expire in {settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS} hours.
        
        If you did not request this, please ignore this email.
        """
        
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            print(f"e[33m[MOCK EMAIL] To: {to_email} | Subject: {subject} | Token: {token}e[0m")
            return

        message = EmailMessage()
        message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True,
        )
