import requests
import time
from notify import send_email   # moduł powiadomień Gmail

def get_klines_15m(symbol="XRPUSDC", limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": "15m",
        "limit": limit
    }
    data = requests.get(url, params=params).json()

    closes = [float(candle[4]) for candle in data]

    return closes[:-1]  # usuń świecę, która jeszcze trwa

def ema(values, period):
    k = 2 / (period + 1)
    ema_val = values[0]
    for price in values[1:]:
        ema_val = price * k + ema_val * (1 - k)
    return ema_val

class StrategyEMA:
    def __init__(self, fast=7, slow=25):
        self.fast = fast
        self.slow = slow
        self.last_signal = None  # do wykrywania zmiany sygnału

    def analyze(self, prices):
        if len(prices) < self.slow + 2:
            return "WAIT"

        ema_fast = ema(prices, self.fast)
        ema_slow = ema(prices, self.slow)

        if ema_fast > ema_slow:
            signal = "BUY (EMA 15m)"
        elif ema_fast < ema_slow:
            signal = "SELL (EMA 15m)"
        else:
            signal = "WAIT"

        # Powiadomienie tylko przy zmianie sygnału
        if signal != self.last_signal:
            send_email(signal)
            self.last_signal = signal

        return signal
