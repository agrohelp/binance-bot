# telegram_alerts.py

import requests
from telegram_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

BOT_TOKEN = TELEGRAM_BOT_TOKEN
CHAT_ID = TELEGRAM_CHAT_ID

last_message_id = None

def send_message(text):
    global last_message_id

    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Telegram: brak BOT_TOKEN lub CHAT_ID (sprawdź .env)")
        return

    # usuń poprzednią wiadomość
    if last_message_id is not None:
        try:
            requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
                params={"chat_id": CHAT_ID, "message_id": last_message_id},
                timeout=5
            )
        except:
            pass

    # wyślij nową
    r = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": text},
        timeout=5
    )

    data = r.json()
    if "result" in data:
        last_message_id = data["result"]["message_id"]


def send_buy_alert(symbol, price):
    send_message(f"🟢 BUY | {symbol} | {price}")

def send_sell_alert(symbol, price):
    send_message(f"🔴 SELL | {symbol} | {price}")

def send_near_cross_alert(symbol, diff):
    send_message(f"⚠️ BLISKO PRZECIĘCIA | {symbol} | różnica: {diff:.5f}")
