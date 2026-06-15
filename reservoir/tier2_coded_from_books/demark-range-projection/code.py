# Engine signal function for 'demark_range_projection' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def demark_range_projection(I, i, htf):
    if i < 1:
        return None
    o = I["open"][i]
    c = I["close"][i]
    lo = I["low"][i]
    hi = I["high"][i]
    pH = I["dm_proj_hi"][i]
    ph = I["high"][i - 1]
    pl = I["low"][i - 1]
    if _nan(o, c, lo, hi, pH, ph, pl):
        return None
    # dm_proj_lo is not precomputed; reconstruct causally.
    # dm_proj_hi = X - prev_low ; dm_proj_lo = X - prev_high
    # => dm_proj_lo = dm_proj_hi - (prev_high - prev_low)
    pL = pH - (ph - pl)
    if lo <= pL and c > pL:
        return "long"
    if hi >= pH and c < pH:
        return "short"
    return None
