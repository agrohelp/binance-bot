import numpy as np
from settings import scalp_ema1, scalp_ema2, delta


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

    # Zamknięte świece
    e1_prev = e1_series[-2]   # EMA fast na świecy -2
    e2_prev = e2_series[-2]   # EMA slow na świecy -2

    e1 = e1_series[-1]        # EMA fast na świecy -1 (zamknięta)
    e2 = e2_series[-1]        # EMA slow na świecy -1 (zamknięta)

    diff_prev = e1_prev - e2_prev
    diff = e1 - e2
    blisko = abs(diff) < delta

    print(
        f"[DEBUG] "
        f"e1_prev={e1_prev:.5f}, e2_prev={e2_prev:.5f} | "
        f"e1={e1:.5f}, e2={e2:.5f} | "
        f"diff_prev={diff_prev:.5f}, diff={diff:.5f} | "
        f"delta={delta:.5f}, blisko={blisko}"
    )

    # 1) BUY — czyste przecięcie z dołu do góry
    if diff_prev < 0 and diff > 0:
        return "BUY", diff, None

    # 2) SELL — czyste przecięcie z góry na dół
    if diff_prev > 0 and diff < 0:
        return "SELL", diff, None

    # 3) BLISKO — EMA są blisko siebie (ale bez przecięcia)
    if blisko:
        if diff > 0:
            return "BLISKO_UP", diff, None
        else:
            return "BLISKO_DOWN", diff, None

    # 4) Brak sygnału
    return None, diff, None
