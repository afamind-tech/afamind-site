from flask import Flask, render_template, request, flash
from services.messaging import send_teams_message 
import secrets
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

BOOKINGS_URL = os.getenv("BOOKINGS_URL", "")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/send-message", methods=["POST"])
def send_message():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not subject or not message:
        flash("Tous les champs obligatoires doivent être renseignés.", "error")
        return render_template("contact.html")

    message_with_subject = f"[Objet : {subject}]\n\n{message}"
    send_teams_message(name, email, message_with_subject)

    flash("Votre message a bien été envoyé sur Teams. Merci !", "success")
    return render_template("confirmation.html", name=name)


@app.route("/rendez-vous")
def rendez_vous():
    return render_template("rendez-vous.html", bookings_url=BOOKINGS_URL)

@app.route("/a-propos")
def a_propos():
    return render_template("a-propos.html")

@app.route("/mentions-legales")
def mentions_legales():
    return render_template("mentions-legales.html")

@app.route("/confidentialite")
def confidentialite():
    return render_template("confidentialite.html")

if __name__ == "__main__":
    app.run(debug=True)




