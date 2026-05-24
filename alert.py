import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHAT_IDS = os.getenv("CHAT_IDS", "")
CHAT_IDS = [int(x.strip()) for x in CHAT_IDS.split(",") if x.strip().isdigit()]

last_messages = {}


def send_message(text):
    global last_messages

    if not BOT_TOKEN or not CHAT_IDS:
        print("❌ Telegram: brak BOT_TOKEN lub CHAT_IDS")
        return

    for chat_id in CHAT_IDS:

        if chat_id in last_messages:
            try:
                requests.get(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
                    params={"chat_id": chat_id, "message_id": last_messages[chat_id]},
                    timeout=5
                )
            except:
                pass

        r = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": chat_id, "text": text},
            timeout=5
        )

        data = r.json()
        if "result" in data:
            last_messages[chat_id] = data["result"]["message_id"]


def send_buy_alert(symbol, price):
    send_message(f"🟢 BUY | {symbol} | {price}")


def send_sell_alert(symbol, price):
    send_message(f"🔴 SELL | {symbol} | {price}")
