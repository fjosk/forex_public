# Engine signal function for 'adx_wakeup_di' (extracted from sister-lab/LAB/backtest/catalog_books.py)
# Form: fn(I, i, htf) -> 'long'|'short'|None. I = dict of precomputed indicator arrays.

def adx_wakeup_di(I, i, htf):
    if i < 11:
        return None
    adx, dp, dm = I["adx"], I["di_plus"], I["di_minus"]
    win = [adx[k] for k in range(i-10, i+1)]
    if any(_nan(x) for x in win):
        return None
    if _nan(adx[i-1], dp[i-1], dm[i-1], dp[i], dm[i]):
        return None
    adx_low = min(win)
    was_below = adx[i-1] < dp[i-1] and adx[i-1] < dm[i-1]
    wake = (adx[i] - adx_low >= 4) and adx[i] > adx[i-1]
    if was_below and wake and dp[i] > dm[i]:
        return "long"
    if was_below and wake and dm[i] > dp[i]:
        return "short"
    return None
