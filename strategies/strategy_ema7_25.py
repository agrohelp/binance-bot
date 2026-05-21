# strategies/ema7_25.py

import numpy as np

def ema(values, period):
    return np.convolve(values, np.ones(period)/period, mode='valid')

def check_signal(prices):
    prices = np.array(prices)

    ema7 = np.convolve(prices, np.ones(7)/7, mode='valid')
    ema25 = np.convolve(prices, np.ones(25)/25, mode='valid')

    # Dopasowanie długości
    min_len = min(len(ema7), len(ema25))
    ema7 = ema7[-min_len:]
    ema25 = ema25[-min_len:]

    # sygnał BUY: EMA7 przebija EMA25 od dołu
    if ema7[-1] > ema25[-1] and ema7[-2] <= ema25[-2]:
        return "BUY"

    # sygnał SELL: EMA7 przebija EMA25 od góry
    if ema7[-1] < ema25[-1] and ema7[-2] >= ema25[-2]:
        return "SELL"

    return None
