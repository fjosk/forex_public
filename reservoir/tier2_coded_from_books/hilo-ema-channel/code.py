# Engine signal function for 'hilo_ema_channel' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def hilo_ema_channel(I, i, htf):
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    hi, hi1 = I["ema_hi13"][i], I["ema_hi13"][i-1]
    lo, lo1 = I["ema_lo13"][i], I["ema_lo13"][i-1]
    if _nan(c, c1, hi, hi1, lo, lo1):
        return None
    if c > hi and c1 <= hi1:
        return "long"
    if c < lo and c1 >= lo1:
        return "short"
    return None
