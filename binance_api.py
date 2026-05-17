import requests
import time

BASE_URL = "https://api.binance.com"

class BinanceAPI:
    def __init__(self):
        pass  # brak kluczy, bo nie handlujemy

    def get_price(self, symbol="BTCUSDT"):
        url = f"{BASE_URL}/api/v3/ticker/price"
        params = {"symbol": symbol}
        r = requests.get(url, params=params)
        return r.json()

    def get_order_book(self, symbol="BTCUSDT", limit=5):
        url = f"{BASE_URL}/api/v3/depth"
        params = {"symbol": symbol, "limit": limit}
        r = requests.get(url, params=params)
        return r.json()

    def get_klines(self, symbol="BTCUSDT", interval="1m", limit=50):
        url = f"{BASE_URL}/api/v3/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        r = requests.get(url, params=params)
        return r.json()
