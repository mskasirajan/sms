"""
Notification utility for SMS, Email, WhatsApp, and Push alerts.
Each function is a stub with the interface defined — replace with
real provider integrations (Twilio, SendGrid, Firebase, etc.).
"""
from app.core.logger import get_logger

logger = get_logger(__name__)


def send_sms(phone: str, message: str) -> bool:
    """Send SMS via provider (e.g. Twilio). Returns True on success."""
    logger.info(f"[SMS] To: {phone} | Message: {message[:80]}...")
    # TODO: integrate Twilio / AWS SNS
    return True


def send_email(to_email: str, subject: str, body_html: str) -> bool:
    """Send email via provider (e.g. SendGrid, SES). Returns True on success."""
    logger.info(f"[EMAIL] To: {to_email} | Subject: {subject}")
    # TODO: integrate SendGrid / AWS SES
    return True


def send_whatsapp(phone: str, message: str) -> bool:
    """Send WhatsApp message via WhatsApp Business API."""
    logger.info(f"[WHATSAPP] To: {phone} | Message: {message[:80]}...")
    # TODO: integrate WhatsApp Business API
    return True


def send_push(device_token: str, title: str, body: str, data: dict = None) -> bool:
    """Send push notification via Firebase FCM."""
    logger.info(f"[PUSH] Token: {device_token[:20]}... | Title: {title}")
    # TODO: integrate Firebase Admin SDK
    return True


# --- High-level helpers ---

def notify_attendance_absent(parent_phone: str, student_name: str, date: str):
    message = f"Dear Parent, {student_name} was marked ABSENT on {date}. Please contact the school if this is incorrect."
    send_sms(parent_phone, message)
    send_whatsapp(parent_phone, message)


def notify_fee_due(parent_phone: str, parent_email: str, student_name: str,
                   invoice_number: str, due_amount: float, due_date: str):
    message = (
        f"Dear Parent, fees of ₹{due_amount:.2f} for {student_name} "
        f"(Invoice: {invoice_number}) are due on {due_date}. Please pay at your earliest convenience."
    )
    send_sms(parent_phone, message)
    send_email(
        parent_email,
        subject=f"Fee Due Reminder — {invoice_number}",
        body_html=f"<p>{message}</p>",
    )


def notify_payment_receipt(parent_email: str, student_name: str,
                            receipt_number: str, amount: float):
    subject = f"Payment Receipt — {receipt_number}"
    body = (
        f"<p>Dear Parent,</p>"
        f"<p>We have received a payment of <strong>₹{amount:.2f}</strong> for {student_name}.</p>"
        f"<p>Receipt Number: <strong>{receipt_number}</strong></p>"
        f"<p>Thank you.</p>"
    )
    send_email(parent_email, subject=subject, body_html=body)
