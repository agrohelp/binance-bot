# strategies/strategy_ema30.py

import pandas as pd

def check_signal(prices):
    if len(prices) < 35:
        return None

    series = pd.Series(prices)
    ema = series.ewm(span=30).mean()

    if series.iloc[-1] > ema.iloc[-1] and series.iloc[-2] <= ema.iloc[-2]:
        return "BUY"

    if series.iloc[-1] < ema.iloc[-1] and series.iloc[-2] >= ema.iloc[-2]:
        return "SELL"

    return None
