import random
import time

def send_email(email: str, campaign_name: str, message: str):
    time.sleep(1)  # simulate network delay

    # Simulate failure
    if random.choice([True, False, False]):
        raise Exception("Email server timeout")

    print(f"Email sent to {email} for campaign {campaign_name}")
