#!/usr/bin/env python3
"""Book-extracted candidate indicators (81 validated + causal). engine.precompute wires the 76 that
a book strategy actually reads (the `_BOOK_INDICATORS` list in engine.py); the other 5 are kept here
as research spares but not computed per-bar."""
import numpy as np
import pandas as pd


def abschg(df):
    close = df['close'].astype(float)
    out = close.diff().abs()
    return out.to_numpy()

def accel(df):
    close = df['close'].astype(float)
    mom = close - close.shift(10)
    out = mom.diff()
    return out.to_numpy()

def asi(df):
    o = df['open'].astype(float).to_numpy()
    h = df['high'].astype(float).to_numpy()
    l = df['low'].astype(float).to_numpy()
    c = df['close'].astype(float).to_numpy()
    n = len(c)
    si = np.full(n, np.nan)
    T = 1.0
    for i in range(1, n):
        C, O = c[i], o[i]
        Cp, Op = c[i-1], o[i-1]
        H, L = h[i], l[i]
        if np.isnan(C) or np.isnan(Cp) or np.isnan(O) or np.isnan(Op) or np.isnan(H) or np.isnan(L):
            continue
        hc = abs(H - Cp); lc = abs(L - Cp); hl = abs(H - L); cpop = abs(Cp - Op)
        if hc >= lc and hc >= hl:
            R = hc - 0.5*lc + 0.25*cpop
        elif lc >= hc and lc >= hl:
            R = lc - 0.5*hc + 0.25*cpop
        else:
            R = hl + 0.25*cpop
        if R == 0 or np.isnan(R):
            si[i] = 0.0
            continue
        K = max(hc, lc)
        num = (C - Cp) + 0.5*(C - O) + 0.25*(Cp - Op)
        si[i] = 50.0 * (num / R) * (K / T)
    out = np.full(n, np.nan)
    started = False
    acc = 0.0
    for i in range(n):
        if np.isnan(si[i]):
            if started:
                out[i] = acc
            continue
        acc += si[i]
        started = True
        out[i] = acc
    return out

def asi_hsp(df):
    o = df['open'].astype(float).to_numpy()
    h = df['high'].astype(float).to_numpy()
    l = df['low'].astype(float).to_numpy()
    c = df['close'].astype(float).to_numpy()
    n = len(c)
    si = np.full(n, np.nan)
    T = 1.0
    for i in range(1, n):
        C, O = c[i], o[i]
        Cp, Op = c[i-1], o[i-1]
        H, L = h[i], l[i]
        if np.isnan(C) or np.isnan(Cp) or np.isnan(O) or np.isnan(Op) or np.isnan(H) or np.isnan(L):
            continue
        hc = abs(H - Cp); lc = abs(L - Cp); hl = abs(H - L); cpop = abs(Cp - Op)
        if hc >= lc and hc >= hl:
            R = hc - 0.5*lc + 0.25*cpop
        elif lc >= hc and lc >= hl:
            R = lc - 0.5*hc + 0.25*cpop
        else:
            R = hl + 0.25*cpop
        if R == 0 or np.isnan(R):
            si[i] = 0.0
            continue
        K = max(hc, lc)
        num = (C - Cp) + 0.5*(C - O) + 0.25*(Cp - Op)
        si[i] = 50.0 * (num / R) * (K / T)
    a = np.full(n, np.nan)
    started = False; acc = 0.0
    for i in range(n):
        if np.isnan(si[i]):
            if started:
                a[i] = acc
            continue
        acc += si[i]; started = True; a[i] = acc
    w = 2
    out = np.full(n, np.nan)
    last = np.nan
    for i in range(n):
        center = i - w
        if center - w >= 0:
            seg = a[center - w: center + w + 1]
            cv = a[center]
            if not np.isnan(cv) and not np.any(np.isnan(seg)):
                if cv == np.max(seg) and cv > seg[0] and cv > seg[-1]:
                    last = cv
        out[i] = last
    return out

def asi_lsp(df):
    o = df['open'].astype(float).to_numpy()
    h = df['high'].astype(float).to_numpy()
    l = df['low'].astype(float).to_numpy()
    c = df['close'].astype(float).to_numpy()
    n = len(c)
    si = np.full(n, np.nan)
    T = 1.0
    for i in range(1, n):
        C, O = c[i], o[i]
        Cp, Op = c[i-1], o[i-1]
        H, L = h[i], l[i]
        if np.isnan(C) or np.isnan(Cp) or np.isnan(O) or np.isnan(Op) or np.isnan(H) or np.isnan(L):
            continue
        hc = abs(H - Cp); lc = abs(L - Cp); hl = abs(H - L); cpop = abs(Cp - Op)
        if hc >= lc and hc >= hl:
            R = hc - 0.5*lc + 0.25*cpop
        elif lc >= hc and lc >= hl:
            R = lc - 0.5*hc + 0.25*cpop
        else:
            R = hl + 0.25*cpop
        if R == 0 or np.isnan(R):
            si[i] = 0.0
            continue
        K = max(hc, lc)
        num = (C - Cp) + 0.5*(C - O) + 0.25*(Cp - Op)
        si[i] = 50.0 * (num / R) * (K / T)
    a = np.full(n, np.nan)
    started = False; acc = 0.0
    for i in range(n):
        if np.isnan(si[i]):
            if started:
                a[i] = acc
            continue
        acc += si[i]; started = True; a[i] = acc
    w = 2
    out = np.full(n, np.nan)
    last = np.nan
    for i in range(n):
        center = i - w
        if center - w >= 0:
            seg = a[center - w: center + w + 1]
            cv = a[center]
            if not np.isnan(cv) and not np.any(np.isnan(seg)):
                if cv == np.min(seg) and cv < seg[0] and cv < seg[-1]:
                    last = cv
        out[i] = last
    return out

def body_mom(df):
    c = df['close'].astype(float)
    o = df['open'].astype(float)
    b = (c - o)
    up = b.clip(lower=0.0)
    dn = (-b).clip(lower=0.0)
    n = 14
    Bup = up.rolling(n).sum()
    Bdown = dn.rolling(n).sum()
    denom = Bup + Bdown
    out = pd.Series(np.nan, index=c.index)
    valid = denom.notna()
    nz = valid & (denom != 0)
    out[nz] = 100.0 * Bup[nz] / denom[nz]
    out[valid & (denom == 0)] = 50.0
    return out.to_numpy()

def buy_swing(df):
    h = df['high'].astype(float)
    o = df['open'].astype(float)
    out = (h - o).rolling(4).mean()
    return out.to_numpy()

def bwmfi(df):
    h = df['high'].astype(float)
    l = df['low'].astype(float)
    v = df['volume'].astype(float)
    eps = 1e-12
    mfi = (h - l) / np.maximum(v.to_numpy(), eps)
    mfi = pd.Series(mfi, index=h.index)
    out = mfi.ewm(span=20, adjust=False).mean()
    return out.to_numpy()

def close_loc(df):
    c = df['close'].astype(float)
    h = df['high'].astype(float)
    l = df['low'].astype(float)
    rng = (h - l)
    out = pd.Series(np.nan, index=c.index)
    valid = rng.notna() & c.notna()
    nz = valid & (rng != 0)
    out[nz] = (c[nz] - l[nz]) / rng[nz]
    out[valid & (rng == 0)] = 0.5
    return out.to_numpy()

def close_loc_sma(df):
    high = df['high'].astype(float)
    low = df['low'].astype(float)
    close = df['close'].astype(float)
    rng = high - low
    clv = ((close - low) - (high - close)) / rng.replace(0, np.nan)
    clv = clv.fillna(0.0)
    return clv.rolling(3).mean().to_numpy()

def close_sma5(df):
    return df['close'].astype(float).rolling(5).mean().to_numpy()

def demand_osc(df):
    high = df['high'].astype(float).to_numpy()
    low = df['low'].astype(float).to_numpy()
    close = df['close'].astype(float).to_numpy()
    vol = df['volume'].astype(float).to_numpy()
    n = len(close)
    tr = np.full(n, np.nan)
    for i in range(1, n):
        tr[i] = max(high[i], high[i-1]) - min(low[i], low[i-1])
    sma_tr = pd.Series(tr).rolling(10).mean().to_numpy()
    bp_sp = np.full(n, np.nan)
    for i in range(1, n):
        if close[i-1] == 0 or np.isnan(sma_tr[i]) or sma_tr[i] == 0:
            continue
        pct = (close[i] - close[i-1]) / close[i-1]
        K = 3.0 * close[i] / sma_tr[i]
        denom = K * abs(pct)
        if close[i] > close[i-1]:
            BP = vol[i]
            SP = vol[i] / denom if denom != 0 else vol[i]
        elif close[i] < close[i-1]:
            SP = vol[i]
            BP = vol[i] / denom if denom != 0 else vol[i]
        else:
            BP = vol[i]
            SP = vol[i]
        bp_sp[i] = BP - SP
    res = pd.Series(bp_sp).ewm(span=10, adjust=False, ignore_na=True).mean().to_numpy()
    res[:1] = np.nan
    return res

def dm_buy_setup(df):
    close = df['close'].astype(float).to_numpy()
    n = len(close)
    out = np.zeros(n)
    cnt = 0
    for i in range(n):
        if i >= 4 and close[i] < close[i-4]:
            cnt += 1
        else:
            cnt = 0
        out[i] = cnt
    if n >= 1:
        out[:min(4, n)] = np.nan
    return out

def dm_buy_countdown(df):
    close = df['close'].astype(float).to_numpy()
    n = len(close)
    setup = np.zeros(n)
    cnt = 0
    for i in range(n):
        if i >= 4 and close[i] < close[i-4]:
            cnt += 1
        else:
            cnt = 0
        setup[i] = cnt
    countdown = np.zeros(n)
    active = False
    cd = 0
    for i in range(n):
        if setup[i] >= 9:
            active = True
            cd = 0
        if active and i >= 2:
            if close[i] <= close[i-2]:
                cd += 1
            if cd >= 13:
                countdown[i] = cd
                active = False
                cd = 0
            else:
                countdown[i] = cd
        else:
            countdown[i] = cd if active else 0
    if n >= 1:
        countdown[:min(4, n)] = np.nan
    return countdown

def dm_proj_hi(df):
    high = df['high'].astype(float).to_numpy()
    low = df['low'].astype(float).to_numpy()
    close = df['close'].astype(float).to_numpy()
    open_ = df['open'].astype(float).to_numpy()
    n = len(close)
    out = np.full(n, np.nan)
    for i in range(1, n):
        Hp, Lp, Cp, Op = high[i-1], low[i-1], close[i-1], open_[i-1]
        if Cp < Op:
            X = (Hp + Cp + 2*Lp) / 2.0
        elif Cp > Op:
            X = (2*Hp + Lp + Cp) / 2.0
        else:
            X = (Hp + Lp + 2*Cp) / 2.0
        out[i] = X - Lp
    return out

def dn_record_count(df):
    low = df['low'].astype(float).to_numpy()
    n = len(low)
    out = np.zeros(n)
    cnt = 0
    for i in range(n):
        if i >= 1 and low[i] < low[i-1]:
            cnt += 1
        else:
            cnt = 0
        out[i] = cnt
    if n >= 1:
        out[:1] = np.nan
    return out

def dow(df):
    return pd.to_datetime(df['open_time'], unit='ms', utc=True).dt.weekday.to_numpy().astype(float)

def drf(df):
    high = df['high'].astype(float).to_numpy()
    low = df['low'].astype(float).to_numpy()
    close = df['close'].astype(float).to_numpy()
    open_ = df['open'].astype(float).to_numpy()
    n = len(close)
    raw = np.full(n, np.nan)
    for i in range(1, n):
        high_g = max(high[i], close[i-1])
        low_g = min(low[i], close[i-1])
        if high_g == low_g:
            raw[i] = 0.5
        else:
            raw[i] = ((high_g - open_[i]) + (close[i] - low_g)) / (2.0 * (high_g - low_g))
    res = pd.Series(raw).ewm(span=3, adjust=False, ignore_na=True).mean().to_numpy()
    res[:1] = np.nan
    return res

def eff_ratio(df):
    close = df['close'].astype(float)
    period = 10
    change = (close - close.shift(period)).abs()
    vol = close.diff().abs().rolling(period).sum()
    er = change / vol.replace(0, np.nan)
    return er.to_numpy()

def ema_hi13(df):
    high = df['high'].astype(float)
    return high.ewm(span=13, adjust=False).mean().to_numpy()

def ema_lo13(df):
    low = df['low'].astype(float)
    return low.ewm(span=13, adjust=False).mean().to_numpy()

def er10(df):
    close = df['close'].astype(float)
    period = 10
    change = (close - close.shift(period)).abs()
    vol = close.diff().abs().rolling(period).sum()
    er = change / vol.replace(0, np.nan)
    return er.to_numpy()

def ewo(df):
    median = (df['high'].astype(float) + df['low'].astype(float)) / 2.0
    fast = median.rolling(5).mean()
    slow = median.rolling(35).mean()
    return (fast - slow).to_numpy()

def filt_pct(df):
    high = df['high'].astype(float)
    low = df['low'].astype(float)
    close = df['close'].astype(float)
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1.0/14, adjust=False).mean()
    atr_pct = 100.0 * atr / close.replace(0, np.nan)
    out = (3.0 * atr_pct).clip(lower=5.0)
    return out.to_numpy()

def force2(df):
    close = df['close'].astype(float)
    volume = df['volume'].astype(float)
    raw = volume * close.diff()
    return raw.ewm(span=2, adjust=False).mean().to_numpy()

def fosc(df):
    close = df['close'].astype(float).to_numpy()
    n = len(close)
    p = 3
    x = np.arange(p, dtype=float)
    xmean = x.mean()
    sxx = ((x - xmean) ** 2).sum()
    tsf = np.full(n, np.nan)
    if sxx > 0:
        for i in range(p - 1, n):
            y = close[i - p + 1:i + 1]
            ymean = y.mean()
            b = ((x - xmean) * (y - ymean)).sum() / sxx
            a = ymean - b * xmean
            tsf[i] = a + b * (p - 1)
    tsf_s = pd.Series(tsf, index=df.index)
    close_s = pd.Series(close, index=df.index)
    osc = 100.0 * (close_s - tsf_s) / close_s.replace(0, np.nan)
    return osc.ewm(span=3, adjust=False).mean().to_numpy()

def frac_dn_bar_high(df):
    high = df['high'].astype(float).to_numpy()
    low = df['low'].astype(float).to_numpy()
    n = len(high)
    out = np.full(n, np.nan)
    last_high = np.nan
    for i in range(n):
        if i >= 4:
            j = i - 2
            lj = low[j]
            if (lj < low[j - 1] and lj < low[j - 2] and lj < low[j + 1] and lj < low[j + 2]):
                last_high = high[j]
        out[i] = last_high
    return out

def frac_up_bar_low(df):
    # Carry-forward LOW of the bar that formed the most recent up-fractal.
    # Up-fractal (Bill Williams 5-bar): high[j] strictly greater than highs at j-2,j-1,j+1,j+2.
    # A fractal at bar j is only CONFIRMED 2 bars later (at j+2), so we detect it then -> causal.
    high = df['high'].to_numpy(dtype=float)
    low = df['low'].to_numpy(dtype=float)
    n = len(df)
    out = np.full(n, np.nan)
    last_low = np.nan
    for k in range(n):
        if k >= 4:
            j = k - 2
            hj = high[j]
            if (hj > high[j-2] and hj > high[j-1] and
                    hj > high[j+1] and hj > high[j+2]):
                last_low = low[j]
        out[k] = last_low
    return out

def hh_n(df, n=10):
    # max(high[i-n .. i-1]); prior-n-bar high, EXCLUDES the current bar.
    return df['high'].astype(float).rolling(n).max().shift(1).to_numpy()

def ll_n(df, n=10):
    # min(low[i-n .. i-1]); prior-n-bar low, EXCLUDES the current bar.
    return df['low'].astype(float).rolling(n).min().shift(1).to_numpy()

def lo_shadow_sma(df, p=14):
    # SMA of lower_shadow over 14. lower_shadow = min(open,close) - low.
    o = df['open'].astype(float)
    c = df['close'].astype(float)
    l = df['low'].astype(float)
    ls = np.minimum(o, c) - l
    return ls.rolling(p).mean().to_numpy()

def lower_shadow(df):
    # min(open,close) - low : per-bar candle lower wick length.
    o = df['open'].to_numpy(dtype=float)
    c = df['close'].to_numpy(dtype=float)
    l = df['low'].to_numpy(dtype=float)
    return np.minimum(o, c) - l

def lr_slope_price(df, p=20):
    # Linear-regression (least-squares) slope of close over a causal rolling window of p=20 bars.
    close = df['close'].astype(float)
    x = np.arange(p, dtype=float)
    x_mean = x.mean()
    xc = x - x_mean
    denom = (xc * xc).sum()
    if denom == 0:
        return np.full(len(df), np.nan)
    def _slope(y):
        if np.isnan(y).any():
            return np.nan
        y_mean = y.mean()
        return (xc * (y - y_mean)).sum() / denom
    return close.rolling(p).apply(_slope, raw=True).to_numpy()

def lr_slope_rsi(df, p=20, rsi_p=14):
    # Linear-regression slope of RSI(14) over a causal rolling window of p=20 bars.
    # RSI uses Wilder's smoothing (standard).
    close = df['close'].astype(float)
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1.0/rsi_p, adjust=False, min_periods=rsi_p).mean()
    avg_loss = loss.ewm(alpha=1.0/rsi_p, adjust=False, min_periods=rsi_p).mean()
    rs = avg_gain / avg_loss.replace(0.0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    # When avg_loss==0 (all gains) RSI=100; when both flat RSI=50.
    rsi = rsi.where(avg_loss != 0.0, 100.0)
    rsi = rsi.where(~((avg_loss == 0.0) & (avg_gain == 0.0)), 50.0)
    rsi = rsi.to_numpy(dtype=float)
    x = np.arange(p, dtype=float)
    x_mean = x.mean()
    xc = x - x_mean
    denom = (xc * xc).sum()
    n = len(df)
    out = np.full(n, np.nan)
    if denom == 0:
        return out
    for i in range(p - 1, n):
        y = rsi[i - p + 1:i + 1]
        if np.isnan(y).any():
            continue
        out[i] = (xc * (y - y.mean())).sum() / denom
    return out

def lrs20(df, N=20):
    # Least-squares slope b of close over last N=20 bars.
    # b = (N*sum(x*y) - sum(x)*sum(y)) / (N*sum(x*x) - sum(x)^2), x=0..N-1.
    close = df['close'].to_numpy(dtype=float)
    n = len(df)
    out = np.full(n, np.nan)
    x = np.arange(N, dtype=float)
    sx = x.sum()
    sxx = (x * x).sum()
    denom = N * sxx - sx * sx
    if denom == 0:
        return out
    for i in range(N - 1, n):
        win = close[i - N + 1:i + 1]
        if np.isnan(win).any():
            continue
        sy = win.sum()
        sxy = (x * win).sum()
        out[i] = (N * sxy - sx * sy) / denom
    return out

def mah3(df, p=3):
    # SMA(high, 3): causal 3-period rolling mean of the high.
    return df['high'].astype(float).rolling(p).mean().to_numpy()

def mal3(df):
    low = pd.to_numeric(df['low'], errors='coerce')
    out = low.rolling(3, min_periods=3).mean()
    return out.to_numpy(dtype=float)

def mdi(df):
    close = pd.to_numeric(df['close'], errors='coerce')
    # cp[i] = 13-period SMA of close ending at bar i (causal)
    cp = close.rolling(13, min_periods=13).mean()
    cp_prev = cp.shift(1)
    denom = (close + close.shift(1)) / 2.0
    denom = denom.replace(0.0, np.nan)
    out = 100.0 * (cp_prev - cp) / denom
    return out.to_numpy(dtype=float)

def mv(df):
    high = pd.to_numeric(df['high'], errors='coerce')
    low = pd.to_numeric(df['low'], errors='coerce')
    close = pd.to_numeric(df['close'], errors='coerce')
    volume = pd.to_numeric(df['volume'], errors='coerce')
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(14, min_periods=14).mean()
    atr_sma = atr.rolling(14, min_periods=14).mean()
    eps = 1e-12
    denom = atr_sma.clip(lower=eps)
    vol_sma = volume.rolling(14, min_periods=14).mean()
    mom = close - close.shift(14)
    out = mom / denom * vol_sma
    return out.to_numpy(dtype=float)

def obtr(df):
    high = pd.to_numeric(df['high'], errors='coerce')
    low = pd.to_numeric(df['low'], errors='coerce')
    close = pd.to_numeric(df['close'], errors='coerce')
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    d = close.diff()
    sgn = np.sign(d.to_numpy())
    sgn = np.nan_to_num(sgn, nan=0.0)
    trv = tr.to_numpy(dtype=float)
    n = len(close)
    out = np.full(n, np.nan, dtype=float)
    if n == 0:
        return out
    running = 0.0
    started = False
    for i in range(n):
        t = trv[i]
        if not np.isfinite(t):
            # no valid true range yet (bar 0): keep NaN, seed at 0 from next valid
            if started:
                out[i] = running
            continue
        if not started:
            running = sgn[i] * t
            started = True
        else:
            running = running + sgn[i] * t
        out[i] = running
    return out

def obtr_ema(df):
    high = pd.to_numeric(df['high'], errors='coerce')
    low = pd.to_numeric(df['low'], errors='coerce')
    close = pd.to_numeric(df['close'], errors='coerce')
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    d = close.diff()
    sgn = np.sign(d.to_numpy())
    sgn = np.nan_to_num(sgn, nan=0.0)
    trv = tr.to_numpy(dtype=float)
    n = len(close)
    obtr_arr = np.full(n, np.nan, dtype=float)
    running = 0.0
    started = False
    for i in range(n):
        t = trv[i]
        if not np.isfinite(t):
            if started:
                obtr_arr[i] = running
            continue
        if not started:
            running = sgn[i] * t
            started = True
        else:
            running = running + sgn[i] * t
        obtr_arr[i] = running
    obtr_s = pd.Series(obtr_arr, index=close.index)
    out = obtr_s.ewm(span=9, adjust=False).mean()
    return out.to_numpy(dtype=float)

def pct_band_lo(df):
    close = pd.to_numeric(df['close'], errors='coerce')
    sma20 = close.rolling(20, min_periods=20).mean()
    out = sma20 * (1.0 - 0.03)
    return out.to_numpy(dtype=float)

def pct_band_up(df):
    close = pd.to_numeric(df['close'], errors='coerce')
    sma20 = close.rolling(20, min_periods=20).mean()
    out = sma20 * (1.0 + 0.03)
    return out.to_numpy(dtype=float)

def prev_swing_lo(df):
    low = pd.to_numeric(df['low'], errors='coerce').to_numpy(dtype=float)
    n = len(low)
    out = np.full(n, np.nan, dtype=float)
    if n == 0:
        return out
    # Williams 5-bar down fractal: low[c] strictly lower than its 2 neighbors each side.
    # A fractal centered at c is only CONFIRMED at bar c+2 (needs 2 future bars).
    # prev_swing_lo[k] = second-most-recent down-fractal price confirmed by bar k.
    last = np.nan      # most recent confirmed down-fractal price
    second = np.nan    # second-most-recent
    for k in range(n):
        c = k - 2  # candidate fractal center whose confirmation completes at bar k
        if c >= 2:
            lc = low[c]
            if (np.isfinite(lc)
                and np.isfinite(low[c-1]) and np.isfinite(low[c-2])
                and np.isfinite(low[c+1]) and np.isfinite(low[c+2])
                and lc < low[c-1] and lc < low[c-2]
                and lc < low[c+1] and lc < low[c+2]):
                second = last
                last = lc
        out[k] = second
    return out

def pvt(df):
    close = pd.to_numeric(df['close'], errors='coerce')
    volume = pd.to_numeric(df['volume'], errors='coerce')
    prev_close = close.shift(1)
    denom = prev_close.replace(0.0, np.nan)
    incr = (volume * (close - prev_close) / denom)
    incr = incr.to_numpy(dtype=float)
    n = len(close)
    out = np.full(n, np.nan, dtype=float)
    running = 0.0
    started = False
    for i in range(n):
        v = incr[i]
        if not np.isfinite(v):
            if started:
                out[i] = running
            continue
        if not started:
            running = v
            started = True
        else:
            running = running + v
        out[i] = running
    return out

def pvt_sma(df):
    close = df['close'].astype(float)
    vol = df['volume'].astype(float)
    prev = close.shift(1)
    chg = (close - prev) / prev.replace(0, np.nan)
    pvt_step = (chg * vol).fillna(0.0)
    pvt = pvt_step.cumsum()
    out = pvt.rolling(21, min_periods=21).mean()
    return out.to_numpy()

def rng5(df):
    high = df['high'].astype(float)
    low = df['low'].astype(float)
    out = high.rolling(5, min_periods=5).max() - low.rolling(5, min_periods=5).min()
    return out.to_numpy()

def rng50(df):
    high = df['high'].astype(float)
    low = df['low'].astype(float)
    out = high.rolling(50, min_periods=50).max() - low.rolling(50, min_periods=50).min()
    return out.to_numpy()

def rng_sma20(df):
    high = df['high'].astype(float)
    low = df['low'].astype(float)
    out = (high - low).rolling(20, min_periods=20).mean()
    return out.to_numpy()

def roc_sd(df):
    close = df['close'].astype(float)
    n = 12
    prev = close.shift(n)
    roc = (close - prev) / prev.replace(0, np.nan) * 100.0
    out = roc.rolling(100, min_periods=100).std()
    return out.to_numpy()

def round_step(df):
    price = df['close'].astype(float).to_numpy()
    out = np.full(len(price), np.nan, dtype=float)
    valid = np.isfinite(price) & (price > 0)
    out[valid] = 10.0 ** np.floor(np.log10(price[valid]) - 1.0)
    return out

def run_ext(df):
    close = df['close'].astype(float).to_numpy()
    n = len(close)
    pct = 0.02
    out = np.full(n, np.nan, dtype=float)
    if n == 0:
        return out
    state = 1  # 1 = long-state, -1 = short-state
    ext = np.nan
    started = False
    for i in range(n):
        c = close[i]
        if not np.isfinite(c):
            out[i] = ext if started else np.nan
            continue
        if not started:
            ext = c
            state = 1
            started = True
            out[i] = ext
            continue
        if state == 1:
            if c > ext:
                ext = c
            elif c <= ext * (1.0 - pct):
                state = -1
                ext = c
        else:
            if c < ext:
                ext = c
            elif c >= ext * (1.0 + pct):
                state = 1
                ext = c
        out[i] = ext
    return out

def sell_swing(df):
    o = df['open'].astype(float)
    low = df['low'].astype(float)
    out = (o - low).rolling(4, min_periods=4).mean()
    return out.to_numpy()

def sma10(df):
    close = df['close'].astype(float)
    out = close.rolling(10, min_periods=10).mean()
    return out.to_numpy()

def sma100(df):
    close = pd.to_numeric(df['close'], errors='coerce')
    return close.rolling(100, min_periods=100).mean().to_numpy()

def sma200(df):
    # Formula field was corrupted (arg-list fragment). Name + used_by (perfect_order_5ma
    # MA ladder 5/20/50/100/200) make this unambiguously SMA(close, 200).
    close = pd.to_numeric(df['close'], errors='coerce')
    return close.rolling(200, min_periods=200).mean().to_numpy()

def sma3_high(df):
    high = pd.to_numeric(df['high'], errors='coerce')
    return high.rolling(3, min_periods=3).mean().to_numpy()

def sma3_low(df):
    low = pd.to_numeric(df['low'], errors='coerce')
    return low.rolling(3, min_periods=3).mean().to_numpy()

def sma_high21(df):
    high = pd.to_numeric(df['high'], errors='coerce')
    return high.rolling(21, min_periods=21).mean().to_numpy()

def sma_low21(df):
    low = pd.to_numeric(df['low'], errors='coerce')
    return low.rolling(21, min_periods=21).mean().to_numpy()

def sroc(df):
    # Smoothed Rate of Change: EMA(close,13) then 21-bar ROC of that EMA, in percent.
    close = pd.to_numeric(df['close'], errors='coerce')
    ema13 = close.ewm(span=13, adjust=False).mean()
    n = 21
    prev = ema13.shift(n)
    out = (ema13 / prev - 1.0) * 100.0
    # guard div-by-zero / non-positive prev
    out = out.where(prev.replace(0.0, np.nan).notna() & (prev != 0.0), np.nan)
    # invalidate warm-up where there is no real prior EMA value
    out.iloc[:n] = np.nan
    return out.to_numpy()

def strength_osc(df):
    # SMA(close - close[1], 14) / SMA(high - low, 14)
    close = pd.to_numeric(df['close'], errors='coerce')
    high = pd.to_numeric(df['high'], errors='coerce')
    low = pd.to_numeric(df['low'], errors='coerce')
    delta = close.diff()  # close - prev close (past), NaN at bar 0
    rng = (high - low)
    num = delta.rolling(14, min_periods=14).mean()
    den = rng.rolling(14, min_periods=14).mean()
    den_safe = den.where(den != 0.0, np.nan)
    out = num / den_safe
    return out.to_numpy()

def tdm(df):
    # Trading-day-of-month: 1-based count of distinct UTC calendar dates seen so far
    # within the current calendar month. Resets when month or year changes.
    ts = pd.to_datetime(df['open_time'], unit='ms', utc=True)
    year = ts.dt.year.to_numpy()
    month = ts.dt.month.to_numpy()
    day = ts.dt.day.to_numpy()
    n = len(df)
    out = np.full(n, np.nan, dtype=float)
    if n == 0:
        return out
    count = 0
    prev_ym = None
    prev_day = None
    for i in range(n):
        if np.isnan(year[i]):
            out[i] = np.nan
            continue
        ym = (int(year[i]), int(month[i]))
        d = int(day[i])
        if ym != prev_ym:
            # new calendar month -> first trading day of this month
            count = 1
            prev_ym = ym
            prev_day = d
        elif d != prev_day:
            # new calendar date within same month -> next trading day
            count += 1
            prev_day = d
        # same date, same month -> intrabar, count unchanged
        out[i] = float(count)
    return out

def thermo(df):
    # max(high-high[1], low[1]-low) if (high>high[1] or low<low[1]) else 0
    high = pd.to_numeric(df['high'], errors='coerce')
    low = pd.to_numeric(df['low'], errors='coerce')
    ph = high.shift(1)
    pl = low.shift(1)
    cond = (high > ph) | (low < pl)
    val = np.maximum(high - ph, pl - low)
    out = np.where(cond.values, val.values, 0.0)
    # warm-up first bar (no prior) -> NaN
    out = out.astype(float)
    out[0] = np.nan
    # where prior was NaN keep NaN
    nanmask = ph.isna().values | pl.isna().values
    out[nanmask] = np.nan
    return out

def thermo_ema(df):
    # EMA(thermo, 22) where thermo = max(high-high[1], low[1]-low) if expansion else 0
    high = pd.to_numeric(df['high'], errors='coerce')
    low = pd.to_numeric(df['low'], errors='coerce')
    ph = high.shift(1)
    pl = low.shift(1)
    cond = (high > ph) | (low < pl)
    val = np.maximum(high - ph, pl - low)
    th = np.where(cond.values, val.values, 0.0).astype(float)
    nanmask = ph.isna().values | pl.isna().values
    th[nanmask] = np.nan
    s = pd.Series(th, index=df.index)
    ema = s.ewm(span=22, adjust=False).mean()
    return ema.values

def tsi(df):
    # True Strength Index: 100 * EMA(EMA(mom,25),13) / EMA(EMA(|mom|,25),13)
    close = pd.to_numeric(df['close'], errors='coerce')
    mom = close.diff()
    amom = mom.abs()
    ema1 = mom.ewm(span=25, adjust=False).mean()
    ema2 = ema1.ewm(span=13, adjust=False).mean()
    aema1 = amom.ewm(span=25, adjust=False).mean()
    aema2 = aema1.ewm(span=13, adjust=False).mean()
    denom = aema2.replace(0, np.nan)
    tsi_val = 100.0 * ema2 / denom
    return tsi_val.values

def tsi_sig(df):
    # EMA(tsi, 7) ; tsi = 100*EMA(EMA(mom,25),13)/EMA(EMA(|mom|,25),13)
    close = pd.to_numeric(df['close'], errors='coerce')
    mom = close.diff()
    amom = mom.abs()
    ema1 = mom.ewm(span=25, adjust=False).mean()
    ema2 = ema1.ewm(span=13, adjust=False).mean()
    aema1 = amom.ewm(span=25, adjust=False).mean()
    aema2 = aema1.ewm(span=13, adjust=False).mean()
    denom = aema2.replace(0, np.nan)
    tsi_val = 100.0 * ema2 / denom
    sig = tsi_val.ewm(span=7, adjust=False).mean()
    return sig.values

def udvo(df):
    # Up/Down Volume Oscillator (window 13):
    # sum_13(vol where close>prev_close) - sum_13(vol where close<prev_close)
    close = pd.to_numeric(df['close'], errors='coerce')
    vol = pd.to_numeric(df['volume'], errors='coerce')
    pc = close.shift(1)
    up_vol = np.where(close.values > pc.values, vol.values, 0.0)
    dn_vol = np.where(close.values < pc.values, vol.values, 0.0)
    up_s = pd.Series(up_vol, index=df.index)
    dn_s = pd.Series(dn_vol, index=df.index)
    osc = up_s.rolling(13).sum() - dn_s.rolling(13).sum()
    return osc.values

def udvo_dn(df):
    # Lower band: SMA(udvo,50) - STD(udvo,50)
    close = pd.to_numeric(df['close'], errors='coerce')
    vol = pd.to_numeric(df['volume'], errors='coerce')
    pc = close.shift(1)
    up_vol = np.where(close.values > pc.values, vol.values, 0.0)
    dn_vol = np.where(close.values < pc.values, vol.values, 0.0)
    up_s = pd.Series(up_vol, index=df.index)
    dn_s = pd.Series(dn_vol, index=df.index)
    osc = up_s.rolling(13).sum() - dn_s.rolling(13).sum()
    sma = osc.rolling(50).mean()
    std = osc.rolling(50).std(ddof=0)
    return (sma - std).values

def udvo_up(df):
    # Upper band: SMA(udvo,50) + STD(udvo,50)
    close = pd.to_numeric(df['close'], errors='coerce')
    vol = pd.to_numeric(df['volume'], errors='coerce')
    pc = close.shift(1)
    up_vol = np.where(close.values > pc.values, vol.values, 0.0)
    dn_vol = np.where(close.values < pc.values, vol.values, 0.0)
    up_s = pd.Series(up_vol, index=df.index)
    dn_s = pd.Series(dn_vol, index=df.index)
    osc = up_s.rolling(13).sum() - dn_s.rolling(13).sum()
    sma = osc.rolling(50).mean()
    std = osc.rolling(50).std(ddof=0)
    return (sma + std).values

def up_record_count(df):
    # Running count of consecutive bars where high[i] > high[i-1]; reset to 0 on non-higher-high.
    high = pd.to_numeric(df['high'], errors='coerce').values
    n = len(high)
    out = np.full(n, np.nan)
    cnt = 0
    for i in range(n):
        if i == 0 or np.isnan(high[i]) or np.isnan(high[i-1]):
            cnt = 0
            out[i] = cnt
            continue
        if high[i] > high[i-1]:
            cnt += 1
        else:
            cnt = 0
        out[i] = cnt
    return out

def up_shadow_sma(df):
    # 14-period SMA of the upper shadow (high minus the higher of open/close)
    upper_shadow = df['high'] - df[['open', 'close']].max(axis=1)
    return upper_shadow.rolling(14).mean().to_numpy()

def upper_shadow(df):
    # Upper wick length: high minus the higher of open/close
    return (df['high'] - df[['open', 'close']].max(axis=1)).to_numpy()

def vavg(df):
    # 35-period SMA of absolute bar-to-bar close change (abschg)
    abschg = df['close'].diff().abs()
    return abschg.rolling(35).mean().to_numpy()

def vci(df):
    # Volume Count Index: cumulative sign of volume change vol[i]-vol[i-1]
    sgn = np.sign(df['volume'].diff().to_numpy())
    sgn = np.where(np.isnan(sgn), 0.0, sgn)
    out = np.cumsum(sgn)
    out[0] = np.nan  # no prior volume at bar 0
    return out

def vci_sma(df):
    # 20-period SMA of the Volume Count Index (cumulative sign of volume change)
    sgn = np.sign(df['volume'].diff())
    sgn = sgn.fillna(0.0)
    vci_series = sgn.cumsum()
    vci_series.iloc[0] = np.nan  # no prior volume at bar 0
    return vci_series.rolling(20).mean().to_numpy()

def vidya(df):
    # Chande's Variable Index Dynamic Average (VIDYA).
    # Volatility index k = stdev(close,9)/stdev(close,30); smoothing constant s=0.20.
    # vidya_t = (k*s)*close_t + (1 - k*s)*vidya_{t-1}
    close = df['close']
    n = len(close)
    s = 0.20
    std9 = close.rolling(9).std(ddof=0)
    std30 = close.rolling(30).std(ddof=0)
    denom = std30.replace(0, np.nan)
    k = (std9 / denom).to_numpy()
    c = close.to_numpy()
    out = np.full(n, np.nan)
    prev = np.nan
    for i in range(n):
        ki = k[i]
        if np.isnan(ki):
            continue
        alpha = ki * s
        if alpha < 0.0:
            alpha = 0.0
        elif alpha > 1.0:
            alpha = 1.0
        if np.isnan(prev):
            prev = c[i]  # seed at first valid bar
        else:
            prev = alpha * c[i] + (1.0 - alpha) * prev
        out[i] = prev
    return out

def vol_sma5(df):
    # 5-period SMA of volume
    return df['volume'].rolling(5).mean().to_numpy()

def vsd(df):
    # 35-period population standard deviation of absolute close change (abschg)
    abschg = df['close'].diff().abs()
    return abschg.rolling(35).std(ddof=0).to_numpy()

def yr_high(df):
    # Rolling 252-bar (approx 1 trading year) maximum of high
    return df['high'].rolling(252).max().to_numpy()

def yr_low(df):
    # Yearly low: lowest low over a trailing 252-bar window (one trading-year lookback).
    # Causal: rolling().min() at bar k uses only bars k-251..k. min_periods=1 so the
    # running minimum is available from the first bar (still strictly backward-looking).
    low = pd.to_numeric(df['low'], errors='coerce')
    n = 252
    out = low.rolling(window=n, min_periods=1).min()
    return out.to_numpy(dtype=float)
