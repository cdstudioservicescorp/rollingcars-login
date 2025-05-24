
from flask import Flask, request, redirect, render_template, session
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.secret_key = 'rollingcars_secret_key'

EMAIL_ORIGEN = "rollingcarsfl.marketing@gmail.com"
EMAIL_DESTINO = "rollingcarsfl.marketing@gmail.com"
EMAIL_PASS = "blxrkqbbxfwwzipo"

@app.route('/')
def home():
    if 'logged' in session:
        return redirect("https://www.rollingcarsusa.com")
    return render_template("login.html")

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    phone = request.form.get('phone', 'Not provided')

    # Enviar correo
    msg = MIMEText(f"Lead captured:\\nEmail: {email}\\nPhone: {phone}")
    msg['Subject'] = 'new leads'
    msg['From'] = EMAIL_ORIGEN
    msg['To'] = EMAIL_DESTINO

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ORIGEN, EMAIL_PASS)
            server.send_message(msg)
        session['logged'] = True
        return redirect("/")
    except Exception as e:
        return f"Error sending email: {e}"

if __name__ == '__main__':
    app.run()
