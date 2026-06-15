# Engine signal function for 'price_acceleration_zero' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def price_acceleration_zero(I, i, htf):
    if i < 1:
        return None
    a, a1 = I["accel"][i], I["accel"][i-1]
    if _nan(a, a1):
        return None
    if a > 0 and a1 <= 0:
        return "long"
    if a < 0 and a1 >= 0:
        return "short"
    return None
