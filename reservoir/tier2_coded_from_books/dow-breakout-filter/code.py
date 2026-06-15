# Engine signal function for 'dow_breakout_filter' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def dow_breakout_filter(I, i, htf):
    if i < 0:
        return None
    c = I["close"][i]
    do = I["day_open"][i]
    dhh = I["prev_dhh"][i]
    dll = I["prev_dll"][i]
    d = I["dow"][i]
    if _nan(c, do, dhh, dll, d):
        return None
    range_y = dhh - dll
    long_trig = c > do + 0.5 * range_y
    short_trig = c < do - 0.5 * range_y
    # dow = ISO weekday Mon=0..Sun=6 (UTC). Longs allowed Mon/Tue/Wed, shorts Thu/Fri.
    if long_trig and d in (0.0, 1.0, 2.0):
        return "long"
    if short_trig and d in (3.0, 4.0):
        return "short"
    return None
