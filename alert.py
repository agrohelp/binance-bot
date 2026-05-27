import requests
import os
from dotenv import load_dotenv
from settings import (
    scalp_symbol,
    scalp_interval,
    scalp_ema1,
    scalp_ema2,
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHAT_IDS = os.getenv("CHAT_IDS", "")
CHAT_IDS = [int(x.strip()) for x in CHAT_IDS.split(",") if x.strip().isdigit()]

# Oddzielne pamięci wiadomości
last_trade_alert = {}   # BUY / SELL / BLISKO
last_test_alert = {}    # TEST ALERT


def send_trade_message(text: str, chat_id: int):
    """BUY/SELL/BLISKO — kasują tylko swoje poprzednie alerty."""
    if chat_id in last_trade_alert:
        try:
            requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
                params={"chat_id": chat_id, "message_id": last_trade_alert[chat_id]},
                timeout=5,
            )
        except:
            pass

    r = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": chat_id, "text": text},
        timeout=5,
    )

    data = r.json()
    if "result" in data:
        last_trade_alert[chat_id] = data["result"]["message_id"]


def send_test_message(text: str, chat_id: int):
    """TEST ALERT — kasuje tylko poprzedni TEST ALERT."""
    if chat_id in last_test_alert:
        try:
            requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
                params={"chat_id": chat_id, "message_id": last_test_alert[chat_id]},
                timeout=5,
            )
        except:
            pass

    r = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": chat_id, "text": text},
        timeout=5,
    )

    data = r.json()
    if "result" in data:
        last_test_alert[chat_id] = data["result"]["message_id"]


# ============================
# ALERTY TRADINGOWE
# ============================

def send_buy_alert(symbol, price, dif=None):
    text = f"📈 BUY — przecięcie EMA\n{symbol} | Cena: {price}"
    for chat_id in CHAT_IDS:
        send_trade_message(text, chat_id)

def send_sell_alert(symbol, price, dif=None):
    text = f"📉 SELL — przecięcie EMA\n{symbol} | Cena: {price}"
    for chat_id in CHAT_IDS:
        send_trade_message(text, chat_id)


def send_blisko_alert(symbol, price, dif, direction: str):
    if direction == "UP":
        text = f"ℹ️ Zbliżenie do BUY (nie sygnał)\n{symbol} | Cena: {price}"
    else:
        text = f"ℹ️ Zbliżenie do SELL (nie sygnał)\n{symbol} | Cena: {price}"

    for chat_id in CHAT_IDS:
        send_trade_message(text, chat_id)


# ============================
# ALERT TESTOWY
# ============================

def send_test_alert(data: dict):
    text = (
        "🧪 TEST EMA - "
        f"{scalp_symbol} | {scalp_interval}\n"
        f"Kierunek: {data['kierunek']}\n"
        f"Blisko: {data['blisko']}"
        f" | Sygnał: {data['signal']}\n"
        f"EMA{scalp_ema1}: {data['e1']:.6f}"
        f" | EMA{scalp_ema2}: {data['e2']:.6f}\n"
        f"Dif: {data['dif']:.6f}"
        f" | Difp: {data['difp']:.6f}\n"
    )

    # # Wysyłamy TEST ALERT do wszystkich chatów, ale nie kasujemy alertów tradingowych
    # for chat_id in CHAT_IDS:
    #     send_test_message(text, chat_id)

    # TEST ALERT tylko dla pierwszej osoby (developer)
    if CHAT_IDS:
        send_test_message(text, CHAT_IDS[0])
