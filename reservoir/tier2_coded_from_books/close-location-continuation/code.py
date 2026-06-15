# Engine signal function for 'close_location_continuation' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def close_location_continuation(I, i, htf):
    if i < 0:
        return None
    h, l, c = I["high"][i], I["low"][i], I["close"][i]
    if _nan(h, l, c):
        return None
    rng = h - l
    clv = (c - l) / rng if rng > 0 else 0.5
    if clv >= 0.65:
        return "long"
    if clv <= 0.35:
        return "short"
    return None
