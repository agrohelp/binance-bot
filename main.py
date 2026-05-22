# main.py

import time
from datetime import datetime
from binance_api import BinanceAPI
from strategy_loader import load_strategy
from telegram_alerts import (
    send_buy_alert,
    send_sell_alert,
    send_near_cross_alert
)

# WYBÓR STRATEGII
STRATEGY_NAME = "ema7_25_pro"

# WYBÓR KRYPTOWALUTY
symbol = "XRPUSDC"

# Załaduj strategię
check_signal = load_strategy(STRATEGY_NAME)
api = BinanceAPI()

print("🚀 Bot startuje...")
print(f"📈 Strategia: {STRATEGY_NAME}")
print(f"💰 Symbol: {symbol}")
print("────────────────────────────────────────────")

first_run = True
last_signal = None
last_candle_time = None

while True:
    try:
        # Pobierz świece 1m
        prices = api.get_prices(symbol, limit=200)

        if not prices or len(prices) < 20:
            print("[WARN] Za mało danych. Czekam...")
            time.sleep(2)
            continue

        # Pobierz timestamp ostatniej świecy
        klines = api.get_klines(symbol, interval="1m", limit=2)
        candle_close_time = klines[-1][6]  # closeTime

        # Jeśli świeca jeszcze się nie zamknęła → czekamy
        if candle_close_time == last_candle_time:
            print(f"⏳ Czekam na zamknięcie świecy | {symbol}")
            time.sleep(2)
            continue

        # Nowa świeca się zamknęła
        last_candle_time = candle_close_time
        current_price = prices[-1]

        print(f"🕒 Nowa świeca zamknięta | Cena: {current_price}")

        # Strategia zwraca: (signal, diff)
        signal, diff = check_signal(prices)

        # Ignoruj pierwszy sygnał po starcie
        if first_run:
            print("⏳ Ignoruję pierwszy sygnał (start bota)")
            first_run = False
            last_signal = signal
            continue

        # Wysyłaj sygnał tylko gdy się zmieni
        if signal != last_signal:

            if signal == "BUY":
                print(f"🟢 BUY | {symbol} | {current_price}")
                send_buy_alert(symbol, current_price)

            elif signal == "SELL":
                print(f"🔴 SELL | {symbol} | {current_price}")
                send_sell_alert(symbol, current_price)

            elif signal == "NEAR_CROSS":
                print(f"⚠️ BLISKO PRZECIĘCIA | różnica: {diff:.5f}")
                send_near_cross_alert(symbol, diff)
            
            last_signal = signal

        else:
            print(f"⏳ Brak nowego sygnału | {symbol} | {current_price}")

        time.sleep(1)

    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(2)
