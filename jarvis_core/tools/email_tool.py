"""Email sending via Gmail SMTP."""
import smtplib
from email.mime.text import MIMEText
from .base import Tool
from ..config import EMAIL_USER, EMAIL_PASS


def _send_email(to: str, subject: str, body: str) -> str:
    if not EMAIL_USER or not EMAIL_PASS:
        return (
            "Email not configured. Set JARVIS_EMAIL_USER and JARVIS_EMAIL_PASS "
            "in .env (use a Gmail App Password)."
        )
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, [to], msg.as_string())
        return f"Email sent to {to}."
    except Exception as e:
        return f"Failed to send email: {e}"


TOOLS = [
    Tool(
        name="send_email",
        description="Send an email via Gmail SMTP. Requires JARVIS_EMAIL_USER/PASS in .env.",
        input_schema={
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email address."},
                "subject": {"type": "string", "description": "Email subject line."},
                "body": {"type": "string", "description": "Email body text."},
            },
            "required": ["to", "subject", "body"],
        },
        handler=_send_email,
    ),
]
