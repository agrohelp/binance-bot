# telegram_alerts.py

import requests

BOT_TOKEN = "TWOJ_BOT_TOKEN"
CHAT_ID = "TWOJ_CHAT_ID"

# zapamiętujemy ID ostatniej wiadomości
last_message_id = None


def send_message(text):
    global last_message_id

    # usuń poprzednią wiadomość, jeśli istnieje
    if last_message_id is not None:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
            params={
                "chat_id": CHAT_ID,
                "message_id": last_message_id
            }
        )

    # wyślij nową wiadomość
    r = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    # zapisz ID nowej wiadomości
    data = r.json()
    if "result" in data:
        last_message_id = data["result"]["message_id"]


def send_buy_alert(symbol, price):
    send_message(f"🟢 BUY | {symbol} | {price}")


def send_sell_alert(symbol, price):
    send_message(f"🔴 SELL | {symbol} | {price}")
