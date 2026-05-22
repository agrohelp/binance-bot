# strategy_ema7_25_pro.py

import pandas as pd

def ema(values, period):
    s = pd.Series(values)
    return s.ewm(span=period, adjust=False).mean()

def check_signal(prices):
    # prices: lista floatów

    if len(prices) < 30:
        return (None, None)

    ema7 = ema(prices, 7)
    ema25 = ema(prices, 25)

    e7_prev = ema7.iloc[-2]
    e25_prev = ema25.iloc[-2]

    e7_now = ema7.iloc[-1]
    e25_now = ema25.iloc[-1]

    # różnica między EMA
    diff = abs(e7_now - e25_now)

    # BUY
    if e7_prev < e25_prev and e7_now > e25_now:
        return ("BUY", None)

    # SELL
    if e7_prev > e25_prev and e7_now < e25_now:
        return ("SELL", None)
    
    # alert blisko przecięcia
    if diff < 0.0010:  # próg dla XRPUSDC
        return ("NEAR_CROSS", diff)
    
    return (None, None)
