import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()  # ładuje .env

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

def send_email(signal):
    msg = MIMEText(f"Nowy sygnał EMA 15m: {signal}")
    msg["Subject"] = "Alert tradingowy EMA 15m"
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)

# # test gmail, po tescie wyłącz
# Test w cmdr: python notify.pt        
# if __name__ == "__main__":
#     send_email("TEST — Gmail działa poprawnie")
#     print("Wysłano testowego maila.")
