# binance_api.py

import requests

BASE_URL = "https://api.binance.com"

class BinanceAPI:
    def __init__(self):
        pass

    def get_price(self, symbol):
        """
        Pobiera aktualną cenę (ostatni trade).
        """
        url = f"{BASE_URL}/api/v3/ticker/price"
        params = {"symbol": symbol}

        r = requests.get(url, params=params)
        data = r.json()

        return float(data["price"])

    def get_prices(self, symbol, limit=100):
        """
        Pobiera listę ostatnich cen zamknięcia (close) z Binance.
        limit = ile świec pobrać (max 1000)
        """
        url = f"{BASE_URL}/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": "1m",
            "limit": limit
        }

        r = requests.get(url, params=params)
        data = r.json()

        closes = [float(candle[4]) for candle in data]
        return closes

    def get_klines(self, symbol, interval="1m", limit=2):
        """
        Pobiera pełne dane świec (OHLC + timestampy).
        """
        url = f"{BASE_URL}/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        r = requests.get(url, params=params)
        return r.json()
