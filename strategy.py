# strategy.py

import importlib

def load_strategy(name: str):
    """
    Dynamicznie ładuje strategię z katalogu strategies/.
    name: np. 'ema15', 'ema30', 'ema7_25', 'rsi'
    """
    module_name = f"strategies.{name}"

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise ValueError(f"Strategia '{name}' nie istnieje.")

    if not hasattr(module, "check_signal"):
        raise ValueError(f"Strategia '{name}' nie ma funkcji check_signal().")

    return module.check_signal
