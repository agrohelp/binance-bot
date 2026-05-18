from strategy_ema import StrategyEMA, get_klines_15m
import time

strategy = StrategyEMA()

while True:
    prices = get_klines_15m("BTCUSDT", 100)
    signal = strategy.analyze(prices)

    print("Sygnał:", signal)

    time.sleep(60)
