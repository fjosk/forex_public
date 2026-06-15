# Engine signal function for 'forecast_oscillator_zero' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def forecast_oscillator_zero(I, i, htf):
    if i < 1:
        return None
    f, f1 = I["fosc"][i], I["fosc"][i-1]
    if _nan(f, f1):
        return None
    if f > 0 and f1 <= 0:
        return "long"
    if f < 0 and f1 >= 0:
        return "short"
    return None
