from flask import Flask, render_template, request, flash
from services.messaging import send_teams_message 
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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

if __name__ == "__main__":
    app.run(debug=True)


