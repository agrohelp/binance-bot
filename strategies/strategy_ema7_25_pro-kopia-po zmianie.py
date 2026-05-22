import pandas as pd

def ema(values, period):
    s = pd.Series(values)
    return s.ewm(span=period, adjust=False).mean()

def check_signal(prices):
    if len(prices) < 30:
        return (None, None)

    ema7 = ema(prices, 7)
    ema25 = ema(prices, 25)

    e7_prev = ema7.iloc[-2]
    e25_prev = ema25.iloc[-2]

    e7_now = ema7.iloc[-1]
    e25_now = ema25.iloc[-1]

    diff = abs(e7_now - e25_now)

    # 1️⃣ BUY
    if e7_prev < e25_prev and e7_now > e25_now:
        return ("BUY", None)

    # 2️⃣ SELL
    if e7_prev > e25_prev and e7_now < e25_now:
        return ("SELL", None)

    # 3️⃣ NEAR_CROSS z kierunkiem
    if diff < 0.0010:
        if e7_now < e25_now:
            return ("NEAR_BUY", diff)
        else:
            return ("NEAR_SELL", diff)

    return (None, None)
