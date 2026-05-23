# scalp.py - Strategia oparta na EMA7 i EMA25 z dodatkowym sygnałem NEAR

import numpy as np

def ema(values, period):
    return np.convolve(values, np.ones(period)/period, mode='valid')[-1]

def check_signal(prices):
    # ceny muszą być float
    prices = [float(p) for p in prices]

    # EMA7 i EMA25
    ema7 = ema(prices, 7)
    ema25 = ema(prices, 25)

    # poprzednie wartości
    ema7_prev = ema(prices[:-1], 7)
    ema25_prev = ema(prices[:-1], 25)

    # różnica
    diff = abs(ema7 - ema25)

    # próg NEAR
    near_threshold = 0.0008

    # DEBUG
    print(f"[DEBUG] e7_prev={ema7_prev:.6f}, e25_prev={ema25_prev:.6f}, "
          f"e7_now={ema7:.6f}, e25_now={ema25:.6f}, diff={diff:.6f}")

    # -------------------------
    # 1️⃣ SYGNAŁ BUY
    # -------------------------
    if ema7_prev < ema25_prev and ema7 > ema25:
        return "BUY", diff

    # -------------------------
    # 2️⃣ SYGNAŁ SELL
    # -------------------------
    if ema7_prev > ema25_prev and ema7 < ema25:
        return "SELL", diff

    # -------------------------
    # 3️⃣ NEAR BUY (zbliżenie od dołu)
    # -------------------------
    if ema7 < ema25 and diff < near_threshold:
        return "NEAR_BUY", diff

    # -------------------------
    # 4️⃣ NEAR SELL (zbliżenie od góry)
    # -------------------------
    if ema7 > ema25 and diff < near_threshold:
        return "NEAR_SELL", diff

    # -------------------------
    # 5️⃣ Brak sygnału
    # -------------------------
    return None, diff
