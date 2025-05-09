import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def enviar_email(destinatario: str, assunto: str, corpo: str):
    msg = MIMEText(corpo)
    msg["Subject"] = assunto
    msg["From"] = os.getenv("MAIL")
    msg["To"] = destinatario

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("MAIL"), os.getenv("PASSWORD"))
        server.send_message(msg)
