import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def send_teams_message(name, email, message_text):
    webhook_url = os.getenv("webhook")
    if not webhook_url:
        raise RuntimeError("Variable d'environnement 'webhook' non configurée")

    payload = {
        "name": name,
        "email": email,
        "message": message_text,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers, timeout=5)

    # Power Automate renvoie 202 (Accepted), donc on accepte 200 ET 202
    if response.status_code not in (200, 202):
        raise ValueError(f"Erreur Teams : {response.status_code} - {response.text}")
