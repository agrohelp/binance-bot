import requests


class BinanceAPI:

    BASE = "https://api.binance.com"

    def get_prices(self, symbol, interval, limit=200):
        url = f"{self.BASE}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        r = requests.get(url, timeout=5)
        data = r.json()
        return [float(x[4]) for x in data]  # close prices


    def get_klines(self, symbol, interval="1m", limit=200):
        url = f"{self.BASE}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        r = requests.get(url, timeout=5)
        return r.json()
