from strategies.scalp import check_signal as scalp_check


def load_strategy(name):
    if name == "scalp":
        return scalp_check
    raise ValueError(f"Nieznana strategia: {name}")
