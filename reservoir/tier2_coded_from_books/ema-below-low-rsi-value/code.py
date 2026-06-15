# Engine signal function for 'ema_below_low_rsi_value' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def ema_below_low_rsi_value(I, i, htf):
    if i < 1:
        return None
    e, r = I["ema20"][i], I["rsi"][i]
    l1, h1 = I["low"][i-1], I["high"][i-1]
    if _nan(e, r, l1, h1):
        return None
    if e < l1 and r < 50:
        return "long"
    if e > h1 and r > 50:
        return "short"
    return None
