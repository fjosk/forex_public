# Engine signal function for 'false_break_failure_fade' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def false_break_failure_fade(I, i, htf):
    if i < 4:
        return None
    h, l, c, du, dl = I["high"], I["low"], I["close"], I["dc_up"], I["dc_lo"]
    if _nan(c[i], c[i-1]):
        return None
    # any bar in i-3..i-1 poked above the PRIOR-bar dc_up, but price is now back below dc_up
    fake_up = any((not _nan(h[j], du[j-1])) and h[j] > du[j-1] for j in range(i-3, i)) \
        and (not _nan(du[i])) and c[i] < du[i]
    fake_dn = any((not _nan(l[j], dl[j-1])) and l[j] < dl[j-1] for j in range(i-3, i)) \
        and (not _nan(dl[i])) and c[i] > dl[i]
    if fake_up and c[i] < c[i-1]:
        return "short"
    if fake_dn and c[i] > c[i-1]:
        return "long"
    return None
