import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
webhook = os.getenv("webhook")

def send_teams_message(name, email, message_text):
    webhook_url = os.getenv("webhook")
    print("WEBHOOK URL =", webhook_url)

    payload = {
        "name": name,
        "email": email,
        "message": message_text,
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        print("STATUS =", response.status_code, "BODY =", response.text)
    except Exception as e:
        print("ERREUR REQUETE TEAMS =", e)
        raise


