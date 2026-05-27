import time
from api import BinanceAPI
from strategies.strategy import load_strategy
from alert import (
    send_buy_alert,
    send_sell_alert,
    send_blisko_alert,
    send_test_alert
)
from settings import scalp_symbol, scalp_interval, scalp_candles, ALERT_TEST_ENABLED

STRATEGY_NAME = "scalp"
symbol = scalp_symbol

check_signal = load_strategy(STRATEGY_NAME)
api = BinanceAPI()

print("🚀 Bot startuje...")
print(f"📈 Strategia: {STRATEGY_NAME}")
print(f"💰 Symbol: {symbol}")
print("────────────────────────────────────────────")

first_run = True
last_candle_time = None
last_signal = None


while True:
    try:
        # Pobranie cen
        prices = api.get_prices(symbol, scalp_interval, limit=scalp_candles)

        if not prices or len(prices) < 20:
            print("[WARN] Za mało danych. Czekam...")
            time.sleep(2)
            continue

        # Pobranie świec
        klines = api.get_klines(symbol, interval=scalp_interval, limit=scalp_candles)
        candle_close_time = klines[-1][6]

        # Czekamy na zamknięcie świecy
        if candle_close_time == last_candle_time:
            print(f"⏳ Czekam na zamknięcie świecy - pauza 120s | {symbol}")
            time.sleep(120)
            continue

        # Nowa świeca
        last_candle_time = candle_close_time
        price = prices[-1]

        # Analiza strategii
        signal, dif, extra = check_signal(prices)

        print(f"🕒 Nowa świeca zamknięta | Cena: {price}")
        print(f"📊 Sygnał: {signal} | Diff: {dif:.8f}")

        # Pierwsza świeca — ignorujemy sygnały tradingowe
        if first_run:
            print("⏳ Ignoruję pierwszy sygnał (start bota)")
            first_run = False
            last_signal = signal

            # TEST ALERT po 1 sekundzie
            if ALERT_TEST_ENABLED:
                time.sleep(1)
                send_test_alert(extra)

            continue

        # ALERTY TRADINGOWE — wysyłane jako pierwsze
        if signal != last_signal:# nie powtarzamy tego samego sygnału

            if signal == "BUY":
                send_buy_alert(symbol, price, dif)

            elif signal == "SELL":
                send_sell_alert(symbol, price, dif)

            elif signal == "BLISKO_UP":# blisko przecięcia BUY
                send_blisko_alert(symbol, price, dif, "UP")

            elif signal == "BLISKO_DOWN":
                send_blisko_alert(symbol, price, dif, "DOWN")

            last_signal = signal

        else:
            print(f"⏳ Brak nowego sygnału | {symbol} | {price}")

        # TEST ALERT — wysyłany ZAWSZE z opoznieniem po 1 sekundzie
        if ALERT_TEST_ENABLED:
            time.sleep(1)
            send_test_alert(extra)

        time.sleep(1)

    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(2)
