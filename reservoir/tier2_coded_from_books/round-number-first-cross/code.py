# Engine signal function for 'round_number_first_cross' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def round_number_first_cross(I, i, htf):
    import math
    if i < 1:
        return None
    c, c1 = I["close"][i], I["close"][i-1]
    h1, l1 = I["high"][i-1], I["low"][i-1]
    step = I["round_step"][i]
    if _nan(c, c1, h1, l1, step) or step <= 0:
        return None
    level = math.ceil(c1 / step) * step
    flr = math.floor(c1 / step) * step
    if c1 < level <= c and h1 < level:
        return "long"
    if c1 > flr >= c and l1 > flr:
        return "short"
    return None
