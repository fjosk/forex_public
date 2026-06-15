# Engine signal function for 'seven_day_streak_fade' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def seven_day_streak_fade(I, i, htf):
    if i < 6:
        return None
    os = I["open"][i-6:i+1]
    cs = I["close"][i-6:i+1]
    if len(os) < 7 or len(cs) < 7:
        return None
    if _nan(*os, *cs):
        return None
    if all(cs[j] < os[j] for j in range(7)):     # seven straight down (red body) candles -> fade long
        return "long"
    if all(cs[j] > os[j] for j in range(7)):     # seven straight up (green body) candles -> fade short
        return "short"
    return None
