# Engine signal function for 'mid_month_fade_short' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def mid_month_fade_short(I, i, htf):
    if i < 0:
        return None
    t = I["tdm"][i]
    c = I["close"][i]
    m = I["sma20"][i]
    if _nan(t, c, m):
        return None
    # tdm = 1-based trading-day-of-month index (UTC). Specific day ordinals act as
    # inflection points, gated by stretch vs SMA20.
    if t == 12.0 and c > m:
        return "short"
    if t in (18.0, 22.0) and c < m:
        return "long"
    return None
