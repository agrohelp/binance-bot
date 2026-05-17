class Strategy:
    def __init__(self):
        self.last_price = None

    def analyze(self, price):
        if self.last_price is None:
            self.last_price = price
            return "WAIT"

        if price > self.last_price:
            signal = "BUY (symulacja)"
        elif price < self.last_price:
            signal = "SELL (symulacja)"
        else:
            signal = "WAIT"

        self.last_price = price
        return signal
