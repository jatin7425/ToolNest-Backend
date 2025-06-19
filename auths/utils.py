from django.conf import settings
from django.core.mail import send_mail


class EmailService:
    """Handles email delivery for the ToolNest platform."""

    @staticmethod
    def send_otp_email(to_email, otp):
        subject = "🔐 Your ToolNest OTP Code"
        message = (
            f"Hello,\n\n"
            f"Your One-Time Password (OTP) is: {otp}\n"
            f"This code is valid for 5 minutes.\n\n"
            f"Stay secure,\nToolNest Team"
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [to_email]

        send_mail(subject, message, from_email, recipient_list)

    # Future-proof: Add more email utilities here
    @staticmethod
    def send_welcome_email(to_email):
        pass  # stubbed for later use
