# Engine signal function for 'nofri_3day_reversal' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def nofri_3day_reversal(I, i, htf):
    if i < 2:
        return None
    adx = I["adx"][i]
    c, c1, c2 = I["close"][i], I["close"][i-1], I["close"][i-2]
    if _nan(adx, c, c1, c2):
        return None
    ranging = adx < 20
    two_down = c < c1 and c1 < c2
    two_up = c > c1 and c1 > c2
    if ranging and two_down:
        return "long"
    if ranging and two_up:
        return "short"
    return None
