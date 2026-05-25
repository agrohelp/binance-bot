import numpy as np
from settings import (
    scalp_symbol,
    scalp_interval,
    scalp_candles,
    scalp_ema1,
    scalp_ema2,
    delta,
    ALERT_TEST_ENABLED
)

def ema_series(values, period):
    values = np.array(values, dtype=float)
    k = 2 / (period + 1)
    ema_vals = [values[0]]

    for price in values[1:]:
        ema_vals.append(price * k + ema_vals[-1] * (1 - k))

    return ema_vals


def check_signal(prices):
    prices = [float(p) for p in prices]

    # EMA
    e1_series = ema_series(prices, scalp_ema1)
    e2_series = ema_series(prices, scalp_ema2)

    e1_prev = e1_series[-2]
    e2_prev = e2_series[-2]

    e1 = e1_series[-1]
    e2 = e2_series[-1]

    diff_prev = e1_prev - e2_prev
    diff = e1 - e2
    blisko = abs(diff) < delta

    print(
        f"[DEBUG] e1_prev={e1_prev:.5f}, e2_prev={e2_prev:.5f} | "
        f"e1={e1:.5f}, e2={e2:.5f} | "
        f"diff_prev={diff_prev:.5f}, diff={diff:.5f} | "
        f"delta={delta:.5f}, blisko={blisko}"
    )

    # sygnał
    signal = None
    if diff_prev < 0 and diff > 0:
        signal = "BUY"
    elif diff_prev > 0 and diff < 0:
        signal = "SELL"
    elif blisko:
        signal = "BLISKO_UP" if diff > diff_prev else "BLISKO_DOWN"

    return signal, diff, {
        "e1": e1,
        "e2": e2,
        "e1_prev": e1_prev,
        "e2_prev": e2_prev,
        "diff": diff,
        "diff_prev": diff_prev,
        "blisko": blisko,
        "signal": signal
    }
