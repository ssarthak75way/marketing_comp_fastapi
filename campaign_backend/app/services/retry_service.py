from app.services.sender_service import send_email
import logging

logger = logging.getLogger(__name__)

def retry_send(email, campaign_name, message, retries=3):
    for attempt in range(retries):
        try:
            send_email(email, campaign_name, message)
            return True
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed for {email} in {campaign_name}: {e}")

    logger.error(f"All {retries} attempts failed for {email} in {campaign_name}")
    return False
