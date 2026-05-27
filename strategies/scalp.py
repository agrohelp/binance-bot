import numpy as np
from datetime import datetime
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
    e1_series = ema_series(prices, scalp_ema1) # EMA7 lista
    e2_series = ema_series(prices, scalp_ema2) # EMA25 lista

    e1 = e1_series[-1] # EMA7 ostatnia (-1) wartość zamkniętej świecy
    e2 = e2_series[-1] # EMA25 ostatnia (-1)  wartość zamkniętej świecy

    e1p = e1_series[-2] # EMA7 wartość świecy (-2) poprzedniej
    e2p = e2_series[-2] # EMA25 wartość świecy (-2) poprzedniej


    dif = e1 - e2 # różnica EMA7 - EMA25 dla ostatniej świecy
    difp = e1p - e2p # różnica EMA7 - EMA25 dla świecy poprzedniej

    #PRZYPISANIA
    # dif>0 → UP/BUY, dif<0 → DOWN/SELL
    dif_up, dif_down, direction, signal = (
        dif, None, "Wzrost", "BUY"
    ) if dif > 0 else (
        None, dif, "Spadek", "SELL"
    )
    # dif_up, dif_down = (dif, None) if dif > 0 else (None, dif)


    # obszar blisko przecięcia (nie sygnał, ale warto obserwować)
    blisko = abs(dif) < delta # true/false

    # print(
    #     f"[DEBUG] e1p={e1p:.5f}, e2p={e2p:.5f} | "
    #     f"e1={e1:.5f}, e2={e2:.5f} | "
    #     f"difp={difp:.5f}, dif={dif:.5f} | "
    #     f"delta={delta:.5f}, blisko={blisko}"
    # )
    # czas = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    czas = datetime.now().strftime("%H:%M")
    print(f"[DEBUG: {czas}] ")
    print(f"e1p={e1p:.5f}, e2p={e2p:.5f}")
    print(f"e1={e1:.5f}, e2={e2:.5f}")
    print(f"difp={difp:.5f}, dif={dif:.5f}")
    print(f"delta={delta:.5f}, blisko={blisko}")

    # sygnał
    signal = None

    # ema7 ost > od poprz i roznica ostatnich e1-e2 >0
    if e1 > e1p and e2 > e2p and dif > 0:
        signal = "BUY"
    elif e1 < e1p and e2 < e2p  and dif < 0:
        signal = "SELL"

    # biez roznica ost < poprz i ema7<ema25
    elif blisko and dif < difp and e1 < e2p:
        signal = "BLISKO_UP"
    elif blisko and dif > difp and e1 > e2p:
        signal = "BLISKO_DOWN"

    return signal, dif, {
        "e1": e1,
        "e2": e2,
        "e1p": e1p,
        "e2p": e2p,
        "dif": dif,
        "difp": difp,
        "blisko": blisko,
        "signal": signal,# BUY, SELL
		"dif_up": dif_up, # kier. UP
		"dif_down": dif_down, # kier. DOWN
		"kierunek": direction # UP, DOWN
    }
