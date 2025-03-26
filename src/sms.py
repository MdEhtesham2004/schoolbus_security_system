from twilio.rest import Client
import os 
from dotenv import load_dotenv
load_dotenv()

ACCOUNT_SID=os.getenv("TWILIO_SID")
AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("FROM_PHNO")
TO_PHONE_NUMBER=os.getenv("TO_PHNO")



def send_sms(phone_number, message):    
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Twilio credentials
    message = f"SchoolSecurity Alert: {message}"
    # Send SMS
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    print(f"Message sent with SID: {message.sid}")
    

