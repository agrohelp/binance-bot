import time
from binance_api import BinanceAPI
from strategy import Strategy

api = BinanceAPI()
strategy = Strategy(api)

def run():
    while True:
        data = api.price("BTCUSDT")
        price = float(data["price"])
        print(f"Cena BTC: {price}")

        if strategy.should_buy(price):
            print("Kupuję...")
            print(api.order_market_buy("BTCUSDT", 0.001))

        if strategy.should_sell(price):
            print("Sprzedaję...")
            print(api.order_market_sell("BTCUSDT", 0.001))

        time.sleep(3)

if __name__ == "__main__":
    run()
