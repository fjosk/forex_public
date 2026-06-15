# Engine signal function for 'dow_two_day_reversal' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def dow_two_day_reversal(I, i, htf):
    if i < 2:
        return None
    c, c1, c2 = I["close"][i], I["close"][i-1], I["close"][i-2]
    d = I["dow"][i]
    if _nan(c, c1, c2, d):
        return None
    up_today = c > c1
    up_yest = c1 > c2
    two_day_up = up_today and up_yest
    two_day_down = (not up_today) and (not up_yest)
    # dow = ISO weekday Mon=0..Sun=6 (UTC). Only fade mid-week (Wed=2, Thu=3).
    if d in (2.0, 3.0):
        if two_day_up:
            return "short"
        if two_day_down:
            return "long"
    return None
