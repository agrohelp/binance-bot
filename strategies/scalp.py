import numpy as np
from settings import scalp_ema1, scalp_ema2, min_diff


def ema_series(values, period):
    values = np.array(values, dtype=float)
    k = 2 / (period + 1)
    ema_vals = [values[0]]

    for price in values[1:]:
        ema_vals.append(price * k + ema_vals[-1] * (1 - k))

    return ema_vals


def check_signal(prices):
    prices = [float(p) for p in prices]

    e1_series = ema_series(prices, scalp_ema1)
    e2_series = ema_series(prices, scalp_ema2)

    e1_last = e1_series[-2]
    e2_last = e2_series[-2]
    e1 = e1_series[-1]
    e2 = e2_series[-1]

    prev_diff = e1_last - e2_last
    curr_diff = e1 - e2
    diff = abs(curr_diff)

    print(f"[DEBUG] prev_diff={prev_diff:.10f}, curr_diff={curr_diff:.10f}, diff={diff:.10f}")

    # BUY: z dołu do góry, z zapasem min_diff
    if prev_diff < -min_diff and curr_diff > min_diff:
        return "BUY", diff, None

    # SELL: z góry na dół, z zapasem min_diff
    if prev_diff > min_diff and curr_diff < -min_diff:
        return "SELL", diff, None

    return None, diff, None
