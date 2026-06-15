# Engine signal function for 'wide_bar_narrow_rest_break' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def wide_bar_narrow_rest_break(I, i, htf):
    if i < 3:
        return None
    h, l, o, c = I["high"], I["low"], I["open"], I["close"]
    w = i - 3
    rs = I["rng_sma20"][i]
    if _nan(rs, h[i], l[i], h[w], l[w], o[w], c[w]):
        return None
    rng_w = h[w] - l[w]
    rest_h = [h[k] for k in range(w + 1, i)]
    rest_l = [l[k] for k in range(w + 1, i)]
    if any(_nan(x) for x in rest_h) or any(_nan(x) for x in rest_l):
        return None
    rest_rng = [rh - rl for rh, rl in zip(rest_h, rest_l)]
    rest_narrow = all(r < rng_w for r in rest_rng)
    wide_up = rng_w > 1.5 * rs and c[w] > o[w]
    if wide_up and rest_narrow and min(rest_l) >= l[w] and h[i] > max(rest_h):
        return "long"
    wide_dn = rng_w > 1.5 * rs and c[w] < o[w]
    if wide_dn and rest_narrow and max(rest_h) <= h[w] and l[i] < min(rest_l):
        return "short"
    return None
