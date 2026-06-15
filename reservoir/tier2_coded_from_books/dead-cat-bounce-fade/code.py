# Engine signal function for 'dead_cat_bounce_fade' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def dead_cat_bounce_fade(I, i, htf):
    r, ap = I["roc"][i], I["atr_pct"][i]
    if _nan(r, ap):
        return None
    thr = max(5.0, 4.0 * ap * 100.0)
    if r >= thr:
        return "short"
    if r <= -thr:
        return "long"
    return None
