# Engine signal function for 'fader_false_break' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def fader_false_break(I, i, htf):
    adx = I["adx"][i]
    c = I["close"][i]
    lo, hi = I["low"][i], I["high"][i]
    pdll, pdhh = I["prev_dll"][i], I["prev_dhh"][i]
    if _nan(adx, c, lo, hi, pdll, pdhh):
        return None
    not_strong = adx < 35
    buf = 0.0015 * c
    if not_strong and lo < pdll - buf and c > pdll:     # poked below prior-day low then closed back inside
        return "long"
    if not_strong and hi > pdhh + buf and c < pdhh:     # poked above prior-day high then closed back inside
        return "short"
    return None
