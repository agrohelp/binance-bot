from binance_api import BinanceAPI
from strategy import Strategy
import time

api = BinanceAPI()
strategy = Strategy()

while True:
    data = api.get_price("XRPUSDC")
    price = float(data["price"])

    signal = strategy.analyze(price)

    print(f"Cena: {price} → Sygnał: {signal}")

    time.sleep(2)
