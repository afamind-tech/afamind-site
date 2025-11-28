import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
webhook = os.getenv("webhook")

def send_teams_message(name, email, message_text):
    webhook_url = webhook

    payload = {
        "text": f"📬 **Nouveau message reçu depuis le site**\n\n👤 *Nom* : {name}\n✉️ *Email* : {email}\n📝 *Message* :\n{message_text}"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Erreur Teams : {response.status_code} - {response.text}")

