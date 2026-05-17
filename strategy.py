class Strategy:
    def __init__(self, api, symbol="BTCUSDT"):
        self.api = api
        self.symbol = symbol

    def should_buy(self, price):
        # PRZYKŁAD: kup jeśli cena < 60k
        return float(price) < 60000

    def should_sell(self, price):
        # PRZYKŁAD: sprzedaj jeśli cena > 70k
        return float(price) > 70000
