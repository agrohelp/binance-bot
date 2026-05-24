import time
from api import BinanceAPI
from strategies.strategy import load_strategy
from alert import send_buy_alert, send_sell_alert
from settings import scalp_symbol, scalp_interval, scalp_candles

STRATEGY_NAME = "scalp"
symbol = scalp_symbol

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
        prices = api.get_prices(symbol, limit=scalp_candles)

        if not prices or len(prices) < 20:
            print("[WARN] Za mało danych. Czekam...")
            time.sleep(2)
            continue

        klines = api.get_klines(symbol, interval=scalp_interval, limit=scalp_candles)
        candle_close_time = klines[-1][6]

        if candle_close_time == last_candle_time:
            print(f"⏳ Czekam na zamknięcie świecy | {symbol}")
            time.sleep(2)
            continue

        last_candle_time = candle_close_time
        current_price = prices[-1]

        print(f"🕒 Nowa świeca zamknięta | Cena: {current_price}")

        signal, diff, _ = check_signal(prices)

        if first_run:
            print("⏳ Ignoruję pierwszy sygnał (start bota)")
            first_run = False
            last_signal = signal
            continue

        if signal != last_signal:

            if signal == "BUY":
                print(f"🟢 BUY | {symbol} | {current_price}")
                send_buy_alert(symbol, current_price)

            elif signal == "SELL":
                print(f"🔴 SELL | {symbol} | {current_price}")
                send_sell_alert(symbol, current_price)

            last_signal = signal

        else:
            print(f"⏳ Brak nowego sygnału | {symbol} | {current_price}")

        time.sleep(1)

    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(2)
