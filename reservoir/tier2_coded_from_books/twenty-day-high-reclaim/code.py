# Engine signal function for 'twenty_day_high_reclaim' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def twenty_day_high_reclaim(I, i, htf):
    if i < 21:
        return None
    h, l, c, du, dl = I["high"], I["low"], I["close"], I["dc_up"], I["dc_lo"]
    if _nan(c[i], c[i-1], l[i-3], h[i-3]):
        return None
    hh_win = [h[k] for k in range(i-20, i)]
    ll_win = [l[k] for k in range(i-20, i)]
    if any(_nan(x) for x in hh_win) or any(_nan(x) for x in ll_win):
        return None
    hh = max(hh_win)
    ll = min(ll_win)
    # long: recently tagged a Donchian high, pulled back, reclaims the 20-bar high THIS bar
    made_high = any((not _nan(h[j], du[j-1])) and h[j] >= du[j-1] for j in range(i-5, i))
    pulled = min(l[i-2], l[i-1], l[i]) < l[i-3]
    reclaim = c[i] > hh and c[i-1] <= hh
    if made_high and pulled and reclaim:
        return "long"
    made_low = any((not _nan(l[j], dl[j-1])) and l[j] <= dl[j-1] for j in range(i-5, i))
    bounced = max(h[i-2], h[i-1], h[i]) > h[i-3]
    reclaim_d = c[i] < ll and c[i-1] >= ll
    if made_low and bounced and reclaim_d:
        return "short"
    return None
