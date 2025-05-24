from flask import Flask, request, redirect, render_template, session
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret')

EMAIL_ORIGEN = os.environ.get("EMAIL_ORIGEN")
EMAIL_DESTINO = os.environ.get("EMAIL_DESTINO")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

@app.route('/')
def home():
    if 'logged' in session:
        return redirect("https://www.rollingcarsusa.com")
    return render_template("login.html")

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    phone = request.form.get('phone', 'Not provided')

    msg = MIMEText(f"Lead captured:\nEmail: {email}\nPhone: {phone}")
    msg['Subject'] = "New Lead"
    msg['From'] = EMAIL_ORIGEN
    msg['To'] = EMAIL_DESTINO

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ORIGEN, EMAIL_PASS)
            server.send_message(msg)
        session['logged'] = True
        return redirect('/')
    except Exception as e:
        return f"Error sending email: {str(e)}"

if __name__ == '__main__':
    app.run()
