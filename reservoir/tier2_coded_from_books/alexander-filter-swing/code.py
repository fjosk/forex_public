# Engine signal function for 'alexander_filter_swing' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def alexander_filter_swing(I, i, htf):
    if i < 1:
        return None
    c = I["close"][i]
    ext1 = I["run_ext"][i-1]
    fp = I["filt_pct"][i]
    if _nan(c, ext1, fp):
        return None
    # NOTE: catalog fns are stateless across calls, so the pseudocode's mutable
    # run_ext / state flip cannot be carried in-function. run_ext is a precomputed
    # running extreme (the swing anchor); a percent-filter flip is detected causally
    # by close clearing last bar's extreme by the dynamic filt_pct band. Long flip =
    # close rises filt_pct% above the prior extreme; short flip = falls filt_pct% below.
    up = ext1 * (1.0 + fp / 100.0)
    dn = ext1 * (1.0 - fp / 100.0)
    if c >= up:
        return "long"
    if c <= dn:
        return "short"
    return None
