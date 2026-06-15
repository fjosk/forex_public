# Engine signal function for 'close_location_momentum' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def close_location_momentum(I, i, htf):
    if i < 1:
        return None
    cl, cl1 = I["close_loc_sma"][i], I["close_loc_sma"][i-1]
    if _nan(cl, cl1):
        return None
    # NOTE: precomputed close_loc_sma is SMA(3) of CLV on the -1..+1 scale
    # ((c-l)-(h-c))/rng, NOT the 0..1 (c-l)/(h-l) the pseudocode assumed.
    # The pseudocode's 0.75/0.25 (0..1) thresholds re-map to +0.5/-0.5 here.
    if cl >= 0.5 and cl1 < 0.5:
        return "long"
    if cl <= -0.5 and cl1 > -0.5:
        return "short"
    return None
