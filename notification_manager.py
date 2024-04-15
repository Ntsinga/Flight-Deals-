import smtplib
from dotenv import load_dotenv, dotenv_values
import requests
from twilio.rest import Client
import os

load_dotenv()
TWILIO_ACC_SID = os.getenv("TWILIO_ACC_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = '+12058721935'
TWILIO_VERIFIED_NUMBER = '+256705549285'
SHEETY_ENDPOINT = "https://api.sheety.co/5c5c46a3644c128e7dea666704bb56cc/flightDeals/users"


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_ACC_SID, TWILIO_AUTH_TOKEN)

    def send_notification(self, message):
        messages = self.client.messages.create(
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER,
            body=message
        )
        print(messages.sid)

    def send_emails(self, message):
        response = requests.get(SHEETY_ENDPOINT)
        member_list = response.json()['users']
        for member in member_list:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user="testingemail641@gmail.com", password="qzzwakpatyydewyu")
                connection.sendmail(
                    from_addr="testingemail641@gmail.com",
                    to_addrs=member['email'],
                    msg=message
                )
