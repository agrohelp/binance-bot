import time, hmac, hashlib, requests
from urllib.parse import urlencode
from config import API_KEY, API_SECRET, BASE_URL

class BinanceAPI:
    def __init__(self):
        self.key = API_KEY
        self.secret = API_SECRET.encode()

    def _sign(self, params):
        query = urlencode(params)
        return hmac.new(self.secret, query.encode(), hashlib.sha256).hexdigest()

    def _get(self, path, params=None, signed=False):
        params = params or {}
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["signature"] = self._sign(params)

        headers = {"X-MBX-APIKEY": self.key}
        r = requests.get(BASE_URL + path, params=params, headers=headers)
        return r.json()

    def _post(self, path, params=None):
        params = params or {}
        params["timestamp"] = int(time.time() * 1000)
        params["signature"] = self._sign(params)

        headers = {"X-MBX-APIKEY": self.key}
        r = requests.post(BASE_URL + path, params=params, headers=headers)
        return r.json()

    # --- PUBLIC ---
    def price(self, symbol):
        return self._get("/api/v3/ticker/price", {"symbol": symbol})

    # --- PRIVATE ---
    def balance(self):
        return self._get("/api/v3/account", signed=True)

    def order_market_buy(self, symbol, qty):
        return self._post("/api/v3/order", {
            "symbol": symbol,
            "side": "BUY",
            "type": "MARKET",
            "quantity": qty
        })

    def order_market_sell(self, symbol, qty):
        return self._post("/api/v3/order", {
            "symbol": symbol,
            "side": "SELL",
            "type": "MARKET",
            "quantity": qty
        })
