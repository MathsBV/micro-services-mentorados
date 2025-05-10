import mysql.connector
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from email_utils import enviar_email
from dotenv import load_dotenv
import os

load_dotenv()

def checar_mentorias():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor(dictionary=True)

    hoje = datetime.now().date()

    # Consulta mentorias do dia que ainda não foram notificadas
    cursor.execute("""
        SELECT *
        FROM Notification
        WHERE DATE(SCHEDULED_DATE) = %s
    """, (hoje,))

    mentorias = cursor.fetchall()

    if not mentorias:
        print(f"[{datetime.now()}] ✅ Nenhuma mentoria para notificar hoje.")
    else:
        for mentoria in mentorias:
            hora = mentoria["SCHEDULED_DATE"].strftime("%H:%M")
            corpo = f"Olá! Sua mentoria é hoje às {hora}."
            try:
                enviar_email(mentoria["MAIL"], f"Lembrete: Mentoria as {hora}", corpo)
                print(f"[{datetime.now()}] ✅ E-mail enviado para {mentoria['MAIL']}")
            except Exception as e:
                print(f"[{datetime.now()}] ❌ Erro ao enviar e-mail para {mentoria['MAIL']}: {e}")
                continue

    print(f"[{datetime.now()}] ✅ Job concluído.\n")

    cursor.close()
    conn.close()

# Roda todo dia às 8h
scheduler = BlockingScheduler()
scheduler.add_job(checar_mentorias, "cron", hour=3, minute=38)
print("🔔 Job agendado para rodar diariamente às 08:00.")
scheduler.start()