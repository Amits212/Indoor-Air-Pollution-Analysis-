from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(message: str):
	client.messages.create(
		from_='+14066921975',
		body=message,
		to='+972586359897'
	)
