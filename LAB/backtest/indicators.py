#!/usr/bin/env python3
"""
Indicators duplicated from TRADE (trade/strategy/indicators.py), vectorised
over the full series so the engine reads precomputed columns instead of an O(n)
recompute per bar. Each function returns the value AT EACH BAR matching what the
TRADE point-function would return when given history up to that bar.

Faithfulness notes (validated against the source in validate_indicators.py):
- RSI / ATR / ADX use Wilder smoothing. TRADE recomputes them on a rolling
  260-bar window each tick; a continuous Wilder pass is identical to ~1e-7 at any
  bar with >~100 bars of history (the seed influence decays over 245+ bars), so
  the continuous form is used.
- Bollinger Bands use POPULATION std (ddof=0), divide by period -- not sample std.
- EMA seeds with the SMA of the first `period` values, then the standard recurrence
  (matches TRADE EMA, not pandas' first-value seed).
- Donchian excludes the current (breakout) bar: max/min of the prior `period` bars.
"""

import os as _os
import sys as _sys

import numpy as np
import pandas as pd

# Single source of truth for the shared indicator math, at FOREX/shared/ (mirrors sister-lab's
# project-root shared/). LAB (this wrapper) AND TRADE both import it, so a strategy's math is
# defined ONCE. _root = the FOREX project root (LAB/backtest -> up 3), which holds `shared/`.
_root = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
if _root not in _sys.path:
    _sys.path.insert(0, _root)
from shared import indicators as _shared  # noqa: E402


def _wilder_run(x: np.ndarray, period: int, first: int) -> np.ndarray:
    """Wilder smoothing of array x (valid from index `first`). Seed = mean of the
    first `period` valid values, placed at index first+period-1; then
    out[i] = (out[i-1]*(period-1) + x[i]) / period."""
    n = len(x)
    out = np.full(n, np.nan)
    seed_end = first + period
    if seed_end > n:
        return out
    seed_idx = first + period - 1
    out[seed_idx] = np.mean(x[first:seed_end])
    prev = out[seed_idx]
    for i in range(seed_end, n):
        prev = (prev * (period - 1) + x[i]) / period
        out[i] = prev
    return out


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    return pd.Series(_shared.wilder_rsi(close.to_numpy(dtype=float), period), index=close.index)


def _true_range(df: pd.DataFrame) -> np.ndarray:
    h = df["high"].to_numpy(); l = df["low"].to_numpy(); c = df["close"].to_numpy()
    pc = np.empty(len(c)); pc[0] = np.nan; pc[1:] = c[:-1]
    tr = np.maximum.reduce([h - l, np.abs(h - pc), np.abs(l - pc)])
    tr[0] = np.nan
    return tr


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    return pd.Series(_shared.atr(df["high"].to_numpy(dtype=float), df["low"].to_numpy(dtype=float),
                                 df["close"].to_numpy(dtype=float), period), index=df.index)


def adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    h = df["high"].to_numpy(); l = df["low"].to_numpy()
    up = np.empty(len(h)); up[0] = np.nan; up[1:] = h[1:] - h[:-1]
    down = np.empty(len(l)); down[0] = np.nan; down[1:] = l[:-1] - l[1:]
    plus_dm = np.where((up > down) & (up > 0), up, 0.0); plus_dm[0] = np.nan
    minus_dm = np.where((down > up) & (down > 0), down, 0.0); minus_dm[0] = np.nan
    tr = _true_range(df)
    atr_s = _wilder_run(tr, period, 1)
    plus_s = _wilder_run(plus_dm, period, 1)
    minus_s = _wilder_run(minus_dm, period, 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        plus_di = np.where(atr_s > 0, 100.0 * plus_s / atr_s, np.nan)
        minus_di = np.where(atr_s > 0, 100.0 * minus_s / atr_s, np.nan)
        di_sum = plus_di + minus_di
        dx = np.where(di_sum > 0, 100.0 * np.abs(plus_di - minus_di) / di_sum, 0.0)
    dx = np.where(np.isnan(atr_s), np.nan, dx)       # dx valid from index `period`
    out = _wilder_run(dx, period, period)            # ADX = Wilder of DX, seeded at 2*period-1
    return pd.Series(out, index=df.index)


def directional_indicators(df: pd.DataFrame, period: int = 14):
    """+DI and -DI (the directional components ADX is built from). Wilder-smoothed."""
    h = df["high"].to_numpy(); l = df["low"].to_numpy()
    up = np.empty(len(h)); up[0] = np.nan; up[1:] = h[1:] - h[:-1]
    down = np.empty(len(l)); down[0] = np.nan; down[1:] = l[:-1] - l[1:]
    plus_dm = np.where((up > down) & (up > 0), up, 0.0); plus_dm[0] = np.nan
    minus_dm = np.where((down > up) & (down > 0), down, 0.0); minus_dm[0] = np.nan
    atr_s = _wilder_run(_true_range(df), period, 1)
    plus_s = _wilder_run(plus_dm, period, 1)
    minus_s = _wilder_run(minus_dm, period, 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        plus_di = np.where(atr_s > 0, 100.0 * plus_s / atr_s, np.nan)
        minus_di = np.where(atr_s > 0, 100.0 * minus_s / atr_s, np.nan)
    return pd.Series(plus_di, index=df.index), pd.Series(minus_di, index=df.index)


def vwap_session(df: pd.DataFrame) -> pd.Series:
    """VWAP anchored to the UTC calendar day. Crypto perps trade 24/7 with no
    session, so the daily anchor is the conventional 24/7 substitute for the
    intraday-session VWAP used in equities. Resets cumulative sums each UTC day."""
    tp = (df["high"] + df["low"] + df["close"]) / 3.0
    vol = df["volume"]
    day = (df["open_time"] // 86_400_000).to_numpy()
    pv = (tp * vol).to_numpy(); v = vol.to_numpy()
    cum_pv = np.zeros(len(v)); cum_v = np.zeros(len(v))
    acc_pv = acc_v = 0.0; cur = None
    for i in range(len(v)):
        if day[i] != cur:
            cur = day[i]; acc_pv = acc_v = 0.0
        acc_pv += pv[i]; acc_v += v[i]
        cum_pv[i] = acc_pv; cum_v[i] = acc_v
    with np.errstate(divide="ignore", invalid="ignore"):
        out = np.where(cum_v > 0, cum_pv / cum_v, np.nan)
    return pd.Series(out, index=df.index)


# =====================================================================
# Round-2 research indicators (textbook-standard formulas, vectorised).
# Non-standard oscillators (WaveTrend, STC, QQE, Fisher, KAMA, SSL,
# HalfTrend, UT Bot, Range Filter) live further down with their formulas.
# =====================================================================

def vortex(df: pd.DataFrame, period: int = 14):
    """Vortex VI+ / VI-. VM+ = |high - prev_low|, VM- = |low - prev_high|,
    normalised by the summed true range over `period`."""
    h = df["high"].to_numpy(); l = df["low"].to_numpy()
    pl = np.empty(len(l)); pl[0] = np.nan; pl[1:] = l[:-1]
    ph = np.empty(len(h)); ph[0] = np.nan; ph[1:] = h[:-1]
    vmp = np.abs(h - pl); vmn = np.abs(l - ph)
    tr = _true_range(df)
    sp = pd.Series(vmp).rolling(period).sum().to_numpy()
    sn = pd.Series(vmn).rolling(period).sum().to_numpy()
    st = pd.Series(tr).rolling(period).sum().to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        vip = np.where(st > 0, sp / st, np.nan)
        vin = np.where(st > 0, sn / st, np.nan)
    return pd.Series(vip, index=df.index), pd.Series(vin, index=df.index)


def aroon(df: pd.DataFrame, period: int = 25):
    """Aroon Up/Down and Oscillator. Up = 100*(period - bars since highest high)/period."""
    hh = df["high"].rolling(period + 1).apply(lambda x: float(np.argmax(x[::-1])), raw=True)
    ll = df["low"].rolling(period + 1).apply(lambda x: float(np.argmin(x[::-1])), raw=True)
    up = 100.0 * (period - hh) / period
    dn = 100.0 * (period - ll) / period
    return up, dn, up - dn


def cmo(close: pd.Series, period: int = 14) -> pd.Series:
    """Chande Momentum Oscillator in [-100, 100]."""
    d = close.diff()
    su = d.clip(lower=0).rolling(period).sum()
    sd = (-d.clip(upper=0)).rolling(period).sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        out = 100.0 * (su - sd) / (su + sd)
    return out


def trix(close: pd.Series, period: int = 15, signal: int = 9):
    """TRIX: 1-bar percent ROC of a triple-EMA-smoothed close, plus its signal line."""
    e1 = _ema_std(close, period); e2 = _ema_std(e1, period); e3 = _ema_std(e2, period)
    tx = 100.0 * (e3 / e3.shift(1) - 1.0)
    return tx, _ema_std(tx, signal)


def awesome_oscillator(df: pd.DataFrame, fast: int = 5, slow: int = 34) -> pd.Series:
    """Awesome Oscillator = SMA(median,5) - SMA(median,34), median = (high+low)/2."""
    med = (df["high"] + df["low"]) / 2.0
    return med.rolling(fast).mean() - med.rolling(slow).mean()


def accelerator(df: pd.DataFrame) -> pd.Series:
    """Accelerator Oscillator = AO - SMA(AO, 5)."""
    ao = awesome_oscillator(df)
    return ao - ao.rolling(5).mean()


def hma(close: pd.Series, period: int = 20) -> pd.Series:
    """Hull MA = WMA(2*WMA(n/2) - WMA(n), sqrt(n)). Smooth + low lag."""
    def wma(s, n):
        w = np.arange(1, n + 1)
        return s.rolling(n).apply(lambda x: np.dot(x, w) / w.sum(), raw=True)
    half = max(1, period // 2); sq = max(1, int(round(period ** 0.5)))
    return wma(2 * wma(close, half) - wma(close, period), sq)


def dema(close: pd.Series, period: int = 20) -> pd.Series:
    """Double EMA = 2*EMA - EMA(EMA)."""
    e = _ema_std(close, period)
    return 2 * e - _ema_std(e, period)


def tema(close: pd.Series, period: int = 20) -> pd.Series:
    """Triple EMA = 3*EMA - 3*EMA(EMA) + EMA(EMA(EMA))."""
    e1 = _ema_std(close, period); e2 = _ema_std(e1, period); e3 = _ema_std(e2, period)
    return 3 * e1 - 3 * e2 + e3


def vwma(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """Volume-weighted moving average."""
    pv = (df["close"] * df["volume"]).rolling(period).sum()
    v = df["volume"].rolling(period).sum()
    return pv / v


def cmf(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """Chaikin Money Flow in [-1, 1]."""
    rng = (df["high"] - df["low"]).replace(0, np.nan)
    mfv = (((df["close"] - df["low"]) - (df["high"] - df["close"])) / rng) * df["volume"]
    return mfv.rolling(period).sum() / df["volume"].rolling(period).sum()


def force_index(df: pd.DataFrame, period: int = 13) -> pd.Series:
    """Elder Force Index = EMA(volume * close_change, period)."""
    raw = df["close"].diff() * df["volume"]
    return _ema_std(raw, period)


def ease_of_movement(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Ease of Movement (Arms), SMA-smoothed."""
    mid = (df["high"] + df["low"]) / 2.0
    dist = mid.diff()
    rng = (df["high"] - df["low"]).replace(0, np.nan)
    box = (df["volume"] / 1e8) / rng
    emv = dist / box.replace(0, np.nan)
    return emv.rolling(period).mean()


def ultimate_oscillator(df: pd.DataFrame, p1: int = 7, p2: int = 14, p3: int = 28) -> pd.Series:
    """Williams Ultimate Oscillator (weighted 4/2/1 across three windows)."""
    c = df["close"]; pc = c.shift(1)
    bp = c - pd.concat([df["low"], pc], axis=1).min(axis=1)
    tr = pd.concat([df["high"], pc], axis=1).max(axis=1) - pd.concat([df["low"], pc], axis=1).min(axis=1)
    def avg(n):
        return bp.rolling(n).sum() / tr.rolling(n).sum().replace(0, np.nan)
    return 100.0 * (4 * avg(p1) + 2 * avg(p2) + avg(p3)) / 7.0


def elder_ray(df: pd.DataFrame, period: int = 13):
    """Elder Ray bull power (high - EMA) and bear power (low - EMA)."""
    e = _ema_std(df["close"], period)
    return df["high"] - e, df["low"] - e


def coppock(close: pd.Series, roc1: int = 14, roc2: int = 11, wma_p: int = 10) -> pd.Series:
    """Coppock Curve = WMA(ROC(roc1) + ROC(roc2), wma_p). Math in shared.indicators."""
    return pd.Series(_shared.coppock(close.to_numpy(dtype=float), roc1, roc2, wma_p), index=close.index)


def kst(close: pd.Series):
    """Know Sure Thing oscillator + its 9-period signal line."""
    def rcma(r, s):
        roc = 100.0 * (close / close.shift(r) - 1.0)
        return roc.rolling(s).mean()
    k = rcma(10, 10) * 1 + rcma(15, 10) * 2 + rcma(20, 10) * 3 + rcma(30, 15) * 4
    return k, k.rolling(9).mean()


def dpo(close: pd.Series, period: int = 20) -> pd.Series:
    """Detrended Price Oscillator: price displaced back vs the SMA."""
    shift = period // 2 + 1
    return close.shift(shift) - close.rolling(period).mean()


def obv(df: pd.DataFrame) -> pd.Series:
    """On-Balance Volume (cumulative signed volume)."""
    sign = np.sign(df["close"].diff().fillna(0.0))
    return (sign * df["volume"]).cumsum()


def ad_line(df: pd.DataFrame) -> pd.Series:
    """Accumulation/Distribution line (cumulative money-flow volume)."""
    rng = (df["high"] - df["low"]).replace(0, np.nan)
    mfv = (((df["close"] - df["low"]) - (df["high"] - df["close"])) / rng) * df["volume"]
    return mfv.fillna(0.0).cumsum()


def chaikin_oscillator(df: pd.DataFrame, fast: int = 3, slow: int = 10) -> pd.Series:
    """Chaikin Oscillator = EMA(A/D,3) - EMA(A/D,10)."""
    ad = ad_line(df)
    return _ema_std(ad, fast) - _ema_std(ad, slow)


def kama(close: pd.Series, period: int = 10, fast: int = 2, slow: int = 30) -> pd.Series:
    """Kaufman Adaptive MA: efficiency-ratio-scaled smoothing constant."""
    arr = close.to_numpy(dtype=float); n = len(arr)
    out = np.full(n, np.nan)
    if n <= period:
        return pd.Series(out, index=close.index)
    change = np.abs(arr[period:] - arr[:-period])
    vol = pd.Series(np.abs(np.diff(arr, prepend=arr[0]))).rolling(period).sum().to_numpy()[period:]
    fsc = 2.0 / (fast + 1.0); ssc = 2.0 / (slow + 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        er = np.where(vol > 0, change / vol, 0.0)
    sc = (er * (fsc - ssc) + ssc) ** 2
    out[period] = arr[period]
    for i in range(period + 1, n):
        out[i] = out[i - 1] + sc[i - period] * (arr[i] - out[i - 1])
    return pd.Series(out, index=close.index)


def fractals(df: pd.DataFrame):
    """Bill Williams 5-bar fractals, CONFIRMED (a fractal centred at i is only known at
    i+2, so the returned boolean is placed at the confirmation bar i+2 -- no look-ahead).
    Returns (up_confirmed, down_confirmed) boolean arrays plus the fractal PRICE."""
    h = df["high"].to_numpy(); l = df["low"].to_numpy(); n = len(h)
    up = np.zeros(n, bool); dn = np.zeros(n, bool)
    up_px = np.full(n, np.nan); dn_px = np.full(n, np.nan)
    for i in range(2, n - 2):
        if h[i] > h[i-1] and h[i] > h[i-2] and h[i] > h[i+1] and h[i] > h[i+2]:
            up[i+2] = True; up_px[i+2] = h[i]               # confirmed 2 bars later
        if l[i] < l[i-1] and l[i] < l[i-2] and l[i] < l[i+1] and l[i] < l[i+2]:
            dn[i+2] = True; dn_px[i+2] = l[i]
    idx = df.index
    return (pd.Series(up, index=idx), pd.Series(dn, index=idx),
            pd.Series(up_px, index=idx).ffill(), pd.Series(dn_px, index=idx).ffill())


def wavetrend(df: pd.DataFrame, n1: int = 10, n2: int = 21):
    """LazyBear WaveTrend. ap=hlc3; esa=EMA(ap,n1); d=EMA(|ap-esa|,n1);
    ci=(ap-esa)/(0.015*d); tci=EMA(ci,n2)=wt1; wt2=SMA(wt1,4)."""
    ap = (df["high"] + df["low"] + df["close"]) / 3.0
    esa = _ema_std(ap, n1)
    d = _ema_std((ap - esa).abs(), n1).replace(0, np.nan)
    ci = (ap - esa) / (0.015 * d)
    wt1 = _ema_std(ci, n2)
    wt2 = wt1.rolling(4).mean()
    return wt1, wt2


def schaff_trend_cycle(close: pd.Series, fast: int = 23, slow: int = 50, cycle: int = 10) -> pd.Series:
    """Schaff Trend Cycle: double stochastic of a MACD line, smoothed (0-100)."""
    macd_line = (_ema_std(close, fast) - _ema_std(close, slow)).to_numpy()
    n = len(macd_line)
    f1 = np.full(n, np.nan); pf = np.full(n, np.nan)
    f2 = np.full(n, np.nan); stc = np.full(n, np.nan)
    for i in range(n):
        if i < cycle:
            continue
        lo = np.nanmin(macd_line[i - cycle + 1:i + 1]); hi = np.nanmax(macd_line[i - cycle + 1:i + 1])
        f1[i] = 100.0 * (macd_line[i] - lo) / (hi - lo) if hi > lo else (pf[i - 1] if i > 0 and not np.isnan(pf[i-1]) else 0.0)
        pf[i] = f1[i] if np.isnan(pf[i - 1]) else pf[i - 1] + 0.5 * (f1[i] - pf[i - 1])
    for i in range(n):
        if i < cycle or np.isnan(pf[i]):
            continue
        win = pf[i - cycle + 1:i + 1]
        lo = np.nanmin(win); hi = np.nanmax(win)
        f2[i] = 100.0 * (pf[i] - lo) / (hi - lo) if hi > lo else (stc[i - 1] if i > 0 and not np.isnan(stc[i-1]) else 0.0)
        stc[i] = f2[i] if (i == 0 or np.isnan(stc[i - 1])) else stc[i - 1] + 0.5 * (f2[i] - stc[i - 1])
    return pd.Series(stc, index=close.index)


def fisher_transform(df: pd.DataFrame, length: int = 9):
    """Ehlers Fisher Transform + its trigger (Fisher shifted one bar)."""
    mid = ((df["high"] + df["low"]) / 2.0).to_numpy()
    n = len(mid)
    v = np.zeros(n); fish = np.zeros(n)
    for i in range(n):
        if i < length:
            continue
        lo = np.min(mid[i - length + 1:i + 1]); hi = np.max(mid[i - length + 1:i + 1])
        raw = 0.0 if hi == lo else 2.0 * ((mid[i] - lo) / (hi - lo) - 0.5)
        v[i] = 0.66 * raw + 0.67 * v[i - 1]
        v[i] = max(min(v[i], 0.999), -0.999)
        fish[i] = 0.5 * np.log((1 + v[i]) / (1 - v[i])) + 0.5 * fish[i - 1]
    fs = pd.Series(fish, index=df.index)
    return fs, fs.shift(1)


def qqe(close: pd.Series, rsi_period: int = 14, smooth: int = 5, factor: float = 4.236):
    """QQE: smoothed RSI (rsiMa) plus a volatility trailing line built from the RSI's
    own ATR. Returns (rsiMa, qqe_line)."""
    rsi_ma, line = _shared.qqe_values(close.to_numpy(dtype=float))
    return pd.Series(rsi_ma, index=close.index), pd.Series(line, index=close.index)


def ssl_channel(df: pd.DataFrame, period: int = 10):
    """SSL channel direction Hlv (+1/-1): close vs SMA(high)/SMA(low) of `period`."""
    sma_hi = df["high"].rolling(period).mean().to_numpy()
    sma_lo = df["low"].rolling(period).mean().to_numpy()
    c = df["close"].to_numpy(); n = len(c)
    hlv = np.full(n, np.nan); prev = 0.0
    for i in range(n):
        if np.isnan(sma_hi[i]):
            continue
        if c[i] > sma_hi[i]:
            prev = 1.0
        elif c[i] < sma_lo[i]:
            prev = -1.0
        hlv[i] = prev
    return pd.Series(hlv, index=df.index)


def ut_bot(df: pd.DataFrame, key: float = 1.0, atr_period: int = 10):
    """UT Bot ATR trailing stop + position (+1 long / -1 short). Flip = entry."""
    c = df["close"].to_numpy()
    nloss = (key * atr(df, atr_period)).to_numpy()
    n = len(c)
    ts = np.full(n, np.nan); pos = np.zeros(n)
    for i in range(1, n):
        if np.isnan(nloss[i]):
            continue
        prev = ts[i - 1]
        if np.isnan(prev):
            ts[i] = c[i] - nloss[i]; pos[i] = 1; continue
        if c[i] > prev and c[i - 1] > prev:
            ts[i] = max(prev, c[i] - nloss[i])
        elif c[i] < prev and c[i - 1] < prev:
            ts[i] = min(prev, c[i] + nloss[i])
        elif c[i] > prev:
            ts[i] = c[i] - nloss[i]
        else:
            ts[i] = c[i] + nloss[i]
        pos[i] = 1 if c[i] > ts[i] else -1
    return pd.Series(ts, index=df.index), pd.Series(pos, index=df.index)


def range_filter(df: pd.DataFrame, period: int = 14, mult: float = 2.618):
    """DW Range Filter line + direction (+1/-1) from a volatility-scaled smoothed range."""
    c = df["close"]
    avrng = _ema_std((c - c.shift(1)).abs(), period)
    smooth = (_ema_std(avrng, 2 * period - 1) * mult).to_numpy()
    cv = c.to_numpy(); n = len(cv)
    filt = np.full(n, np.nan); direction = np.zeros(n)
    for i in range(1, n):
        if np.isnan(smooth[i]):
            continue
        prev = filt[i - 1]
        if np.isnan(prev):
            filt[i] = cv[i]; continue
        if cv[i] > prev:
            filt[i] = max(prev, cv[i] - smooth[i])
        else:
            filt[i] = min(prev, cv[i] + smooth[i])
        direction[i] = 1 if filt[i] > prev else (-1 if filt[i] < prev else direction[i - 1])
    return pd.Series(filt, index=df.index), pd.Series(direction, index=df.index)


def chande_kroll(df: pd.DataFrame, p: int = 10, x: float = 1.0, q: int = 9):
    """Chande Kroll stop: stop_long (below) and stop_short (above)."""
    a = atr(df, p)
    first_high = df["high"].rolling(p).max() - x * a
    first_low = df["low"].rolling(p).min() + x * a
    stop_short = first_high.rolling(q).max()
    stop_long = first_low.rolling(q).min()
    return stop_long, stop_short


def chandelier_dir(df: pd.DataFrame, period: int = 22, mult: float = 3.0) -> pd.Series:
    """Chandelier Exit direction (+1/-1): close vs the ratcheting long/short stops."""
    a = atr(df, period).to_numpy()
    hh = df["high"].rolling(period).max().to_numpy()
    ll = df["low"].rolling(period).min().to_numpy()
    c = df["close"].to_numpy(); n = len(c)
    long_stop = np.full(n, np.nan); short_stop = np.full(n, np.nan)
    direction = np.zeros(n); prev = 1.0
    for i in range(n):
        if np.isnan(a[i]):
            continue
        ls = hh[i] - mult * a[i]; ss = ll[i] + mult * a[i]
        if i > 0 and not np.isnan(long_stop[i - 1]):
            ls = max(ls, long_stop[i - 1]) if c[i - 1] > long_stop[i - 1] else ls
            ss = min(ss, short_stop[i - 1]) if c[i - 1] < short_stop[i - 1] else ss
        long_stop[i] = ls; short_stop[i] = ss
        if c[i] > (short_stop[i - 1] if i > 0 and not np.isnan(short_stop[i-1]) else ss):
            prev = 1.0
        elif c[i] < (long_stop[i - 1] if i > 0 and not np.isnan(long_stop[i-1]) else ls):
            prev = -1.0
        direction[i] = prev
    return pd.Series(direction, index=df.index)


def bbw_percentile(close: pd.Series, period: int = 20, lookback: int = 120) -> pd.Series:
    """Bollinger Band Width as a rolling percentile rank (0-100) over `lookback`."""
    mid = close.rolling(period).mean()
    dev = close.rolling(period).std(ddof=0)
    bbw = (2 * dev) / mid
    return bbw.rolling(lookback).apply(
        lambda x: 100.0 * (x[-1] > x[:-1]).sum() / max(len(x) - 1, 1), raw=True)


def klinger(df: pd.DataFrame):
    """Klinger Volume Oscillator + signal. Volume force with trend-reset cumulative range."""
    hlc = ((df["high"] + df["low"] + df["close"]) / 3.0).to_numpy()
    dm = (df["high"] - df["low"]).to_numpy()
    vol = df["volume"].to_numpy(); n = len(hlc)
    trend = np.zeros(n); cm = np.zeros(n); vf = np.zeros(n)
    for i in range(1, n):
        trend[i] = 1.0 if hlc[i] > hlc[i - 1] else -1.0
        cm[i] = (cm[i - 1] + dm[i]) if trend[i] == trend[i - 1] else (dm[i - 1] + dm[i])
        ratio = abs(2.0 * (dm[i] / cm[i] - 1.0)) if cm[i] != 0 else 0.0
        vf[i] = vol[i] * ratio * trend[i] * 100.0
    vfs = pd.Series(vf, index=df.index)
    kvo = _ema_std(vfs, 34) - _ema_std(vfs, 55)
    return kvo, _ema_std(kvo, 13)


def camarilla_pivots(df: pd.DataFrame):
    """Camarilla R3/R4/S3/S4 from the prior UTC day's H/L/C (the reversion + breakout
    lines). Forward-filled across the current day; no look-ahead."""
    _, p_hh, p_ll, _, _ = utc_day_features(df)        # prior-day H/L
    pp = _prev_day_close(df)                           # prior-day close
    rng = p_hh - p_ll
    r3 = pp + rng * 1.1 / 4.0; r4 = pp + rng * 1.1 / 2.0
    s3 = pp - rng * 1.1 / 4.0; s4 = pp - rng * 1.1 / 2.0
    return r3, r4, s3, s4


def _prev_day_close(df: pd.DataFrame):
    ot = df["open_time"].to_numpy(); c = df["close"].to_numpy()
    day = ot // 86_400_000; n = len(c)
    out = np.full(n, np.nan); cur = None; d_lc = np.nan; p_cc = np.nan
    for i in range(n):
        if day[i] != cur:
            if cur is not None:
                p_cc = d_lc
            cur = day[i]
        d_lc = c[i]
        out[i] = p_cc
    return out


def utc_day_features(df: pd.DataFrame):
    """Per-bar UTC-calendar-day anchors for session-style strategies adapted to
    24/7 perps: the open of the current UTC day (forward-filled across its bars),
    and the previous UTC day's HH/LL/highest-close/lowest-close. Returns five
    numpy arrays aligned to df. The 00:00-UTC anchor is the conventional 24/7
    substitute for an equities session open."""
    ot = df["open_time"].to_numpy()
    o = df["open"].to_numpy(); h = df["high"].to_numpy()
    l = df["low"].to_numpy(); c = df["close"].to_numpy()
    day = ot // 86_400_000
    n = len(c)
    day_open = np.full(n, np.nan)
    prev_hh = np.full(n, np.nan); prev_ll = np.full(n, np.nan)
    prev_hc = np.full(n, np.nan); prev_lc = np.full(n, np.nan)
    cur = None; cur_open = np.nan
    p_hh = p_ll = p_hc = p_lc = np.nan          # previous completed day's stats
    d_hh = d_ll = d_hc = d_lc = np.nan          # current day's running stats
    for i in range(n):
        if day[i] != cur:
            # day rolled over: promote the just-finished day's stats to "previous"
            if cur is not None:
                p_hh, p_ll, p_hc, p_lc = d_hh, d_ll, d_hc, d_lc
            cur = day[i]; cur_open = o[i]
            d_hh = h[i]; d_ll = l[i]; d_hc = c[i]; d_lc = c[i]
        else:
            d_hh = max(d_hh, h[i]); d_ll = min(d_ll, l[i])
            d_hc = max(d_hc, c[i]); d_lc = min(d_lc, c[i])
        day_open[i] = cur_open
        prev_hh[i] = p_hh; prev_ll[i] = p_ll; prev_hc[i] = p_hc; prev_lc[i] = p_lc
    return day_open, prev_hh, prev_ll, prev_hc, prev_lc


def daily_pivots(df: pd.DataFrame):
    """Classic floor-trader pivots from the PREVIOUS UTC day's H/L/C, forward-filled
    onto each bar of the current day. 24/7 perps have no session, so the UTC day is the
    conventional anchor. Returns (P, R1, S1, R2, S2) numpy arrays. No look-ahead: each
    day's pivots use only the prior completed day."""
    ot = df["open_time"].to_numpy()
    h = df["high"].to_numpy(); l = df["low"].to_numpy(); c = df["close"].to_numpy()
    day = ot // 86_400_000
    n = len(c)
    P = np.full(n, np.nan); R1 = np.full(n, np.nan); S1 = np.full(n, np.nan)
    R2 = np.full(n, np.nan); S2 = np.full(n, np.nan)
    cur = None
    d_hh = d_ll = d_lc = np.nan          # current day's running H/L/last-close
    p_hh = p_ll = p_cc = np.nan          # previous completed day's H/L/close
    for i in range(n):
        if day[i] != cur:
            if cur is not None:
                p_hh, p_ll, p_cc = d_hh, d_ll, d_lc      # promote finished day
            cur = day[i]; d_hh = h[i]; d_ll = l[i]
        else:
            d_hh = max(d_hh, h[i]); d_ll = min(d_ll, l[i])
        d_lc = c[i]
        if not np.isnan(p_cc):
            p = (p_hh + p_ll + p_cc) / 3.0
            P[i] = p; R1[i] = 2 * p - p_ll; S1[i] = 2 * p - p_hh
            R2[i] = p + (p_hh - p_ll); S2[i] = p - (p_hh - p_ll)
    return P, R1, S1, R2, S2


def ema(values: pd.Series, period: int) -> pd.Series:
    return pd.Series(_shared.ema(values.to_numpy(dtype=float), period), index=values.index)


def sma(values: pd.Series, period: int) -> pd.Series:
    return values.rolling(period).mean()


def bollinger(close: pd.Series, period: int = 20, std_mult: float = 2.0):
    mid = close.rolling(period).mean()
    std = close.rolling(period).std(ddof=0)          # POPULATION std (matches source)
    return mid, mid - std_mult * std, mid + std_mult * std


def sma_trend_direction(close: pd.Series, period: int = 200, slope_lookback: int = 5) -> pd.Series:
    s = close.rolling(period).mean()
    slope = s - s.shift(slope_lookback)
    out = np.sign(slope)                              # +1 / -1 / 0
    return pd.Series(out, index=close.index).fillna(0.0)


def donchian(df: pd.DataFrame, period: int = 20):
    """Channel of the `period` bars BEFORE the current bar (current excluded)."""
    upper = df["high"].rolling(period).max().shift(1)
    lower = df["low"].rolling(period).min().shift(1)
    return upper, lower


def avg_volume(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """20-bar average volume. TRADE divides by min(len,20); with full history
    that is just the rolling mean once `period` bars exist."""
    return df["volume"].rolling(period).mean()


def day_volume_usd(df: pd.DataFrame) -> pd.Series:
    """Proxy for live dayNtlVlm: rolling 24h notional from quote_volume (1h bars)."""
    return df["quote_volume"].rolling(24).sum()


# =====================================================================
# Extended indicators for the sister-lab/backtest strategy library (BTCSTRAT + BINOPT).
# All vectorised; iterative ones (Supertrend, PSAR) loop once over the series.
# Conventional MACD/Stoch use the standard textbook definitions.
# =====================================================================

def _ema_std(s: pd.Series, span: int) -> pd.Series:
    """Conventional EMA (first-value seed) for MACD-family use."""
    return s.ewm(span=span, adjust=False).mean()


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    line, sig, hist = _shared.macd(close.to_numpy(dtype=float), fast, slow, signal)
    i = close.index
    return pd.Series(line, index=i), pd.Series(sig, index=i), pd.Series(hist, index=i)


def stochastic(df: pd.DataFrame, k_period: int = 14, k_smooth: int = 3, d_smooth: int = 3):
    ll = df["low"].rolling(k_period).min()
    hh = df["high"].rolling(k_period).max()
    rng = (hh - ll).replace(0, np.nan)
    raw_k = 100 * (df["close"] - ll) / rng
    k = raw_k.rolling(k_smooth).mean()
    d = k.rolling(d_smooth).mean()
    return k, d


def _smma(s: pd.Series, period: int) -> pd.Series:
    """Wilder/smoothed MA (RMA): SMA seed then alpha=1/period recurrence."""
    arr = s.to_numpy(dtype=float)
    out = np.full(len(arr), np.nan)
    if len(arr) < period:
        return pd.Series(out, index=s.index)
    out[period - 1] = np.nanmean(arr[:period])
    a = 1.0 / period
    for i in range(period, len(arr)):
        prev = out[i - 1]
        out[i] = prev + a * (arr[i] - prev)
    return pd.Series(out, index=s.index)


def alligator(df: pd.DataFrame, jaw=13, teeth=8, lips=5, jaw_sh=8, teeth_sh=5, lips_sh=3):
    """Standard Bill Williams Alligator on median price; lines shifted forward."""
    med = (df["high"] + df["low"]) / 2.0
    jaw_l = _smma(med, jaw).shift(jaw_sh)
    teeth_l = _smma(med, teeth).shift(teeth_sh)
    lips_l = _smma(med, lips).shift(lips_sh)
    return jaw_l, teeth_l, lips_l


def supertrend(df: pd.DataFrame, period: int = 10, mult: float = 3.0):
    """Supertrend line + direction (+1 uptrend / -1 downtrend). Standard algorithm."""
    atr_s = atr(df, period).to_numpy()
    hl2 = ((df["high"] + df["low"]) / 2.0).to_numpy()
    close = df["close"].to_numpy()
    n = len(close)
    upper = hl2 + mult * atr_s
    lower = hl2 - mult * atr_s
    fin_up = np.full(n, np.nan)
    fin_lo = np.full(n, np.nan)
    direction = np.ones(n)            # +1 up / -1 down
    for i in range(1, n):
        if np.isnan(atr_s[i]):
            continue
        fin_up[i] = upper[i] if (np.isnan(fin_up[i-1]) or upper[i] < fin_up[i-1] or close[i-1] > fin_up[i-1]) else fin_up[i-1]
        fin_lo[i] = lower[i] if (np.isnan(fin_lo[i-1]) or lower[i] > fin_lo[i-1] or close[i-1] < fin_lo[i-1]) else fin_lo[i-1]
        prev_dir = direction[i-1]
        if close[i] > (fin_up[i-1] if not np.isnan(fin_up[i-1]) else upper[i]):
            direction[i] = 1
        elif close[i] < (fin_lo[i-1] if not np.isnan(fin_lo[i-1]) else lower[i]):
            direction[i] = -1
        else:
            direction[i] = prev_dir
    line = np.where(direction == 1, fin_lo, fin_up)
    return pd.Series(line, index=df.index), pd.Series(direction, index=df.index)


def psar(df: pd.DataFrame, step: float = 0.02, max_step: float = 0.2):
    """Parabolic SAR value + trend (+1 long / -1 short). Standard Wilder algorithm."""
    high = df["high"].to_numpy(); low = df["low"].to_numpy()
    n = len(high)
    sar = np.full(n, np.nan); trend = np.ones(n)
    if n < 2:
        return pd.Series(sar, index=df.index), pd.Series(trend, index=df.index)
    up = True
    af = step
    ep = high[0]
    sar[0] = low[0]
    for i in range(1, n):
        prev = sar[i-1]
        if up:
            cur = prev + af * (ep - prev)
            cur = min(cur, low[i-1], low[i-2] if i >= 2 else low[i-1])
            if low[i] < cur:                 # flip to down
                up = False; cur = ep; ep = low[i]; af = step
            else:
                if high[i] > ep:
                    ep = high[i]; af = min(af + step, max_step)
        else:
            cur = prev + af * (ep - prev)
            cur = max(cur, high[i-1], high[i-2] if i >= 2 else high[i-1])
            if high[i] > cur:                # flip to up
                up = True; cur = ep; ep = high[i]; af = step
            else:
                if low[i] < ep:
                    ep = low[i]; af = min(af + step, max_step)
        sar[i] = cur
        trend[i] = 1 if up else -1
    return pd.Series(sar, index=df.index), pd.Series(trend, index=df.index)


def ichimoku(df: pd.DataFrame, tenkan=9, kijun=26, senkou_b=52, disp=26):
    """Tenkan, Kijun, and the forward-shifted cloud spans A/B (decision-time aligned)."""
    h, l = df["high"], df["low"]
    ten = (h.rolling(tenkan).max() + l.rolling(tenkan).min()) / 2.0
    kij = (h.rolling(kijun).max() + l.rolling(kijun).min()) / 2.0
    span_a = ((ten + kij) / 2.0).shift(disp)
    span_b = ((h.rolling(senkou_b).max() + l.rolling(senkou_b).min()) / 2.0).shift(disp)
    return ten, kij, span_a, span_b


# =====================================================================
# Extended indicators for the research-expansion strategy catalog.
# Conventional textbook definitions; vectorised over the full series.
# =====================================================================

def keltner(df: pd.DataFrame, period: int = 20, mult: float = 2.0, atr_period: int = 10):
    """Keltner Channel: EMA(close,period) center, +/- mult*ATR(atr_period) bands."""
    mid = _ema_std(df["close"], period)
    rng = atr(df, atr_period)
    return mid, mid - mult * rng, mid + mult * rng


def cci(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """Commodity Channel Index. Mean deviation in the denominator (textbook)."""
    tp = (df["high"] + df["low"] + df["close"]) / 3.0
    sma_tp = tp.rolling(period).mean()
    mad = tp.rolling(period).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        out = (tp - sma_tp) / (0.015 * mad)
    return out


def williams_r(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Williams %R in [-100, 0]. -100 = period low, 0 = period high."""
    hh = df["high"].rolling(period).max()
    ll = df["low"].rolling(period).min()
    rng = (hh - ll).replace(0, np.nan)
    return -100.0 * (hh - df["close"]) / rng


def mfi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Money Flow Index (volume-weighted RSI) in [0, 100]."""
    tp = (df["high"] + df["low"] + df["close"]) / 3.0
    rmf = tp * df["volume"]
    dtp = tp.diff()
    pos = rmf.where(dtp > 0, 0.0).rolling(period).sum()
    neg = rmf.where(dtp < 0, 0.0).rolling(period).sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = pos / neg
        out = 100.0 - 100.0 / (1.0 + ratio)
    out = out.where(neg != 0, 100.0)              # no negative flow -> MFI 100
    return out


def stoch_rsi(close: pd.Series, rsi_period: int = 14, stoch_period: int = 14,
              k_smooth: int = 3, d_smooth: int = 3):
    """Stochastic RSI: %K/%D of RSI over its own min/max window, scaled 0-100."""
    r = rsi(close, rsi_period)
    ll = r.rolling(stoch_period).min()
    hh = r.rolling(stoch_period).max()
    rng = (hh - ll).replace(0, np.nan)
    raw = 100.0 * (r - ll) / rng
    k = raw.rolling(k_smooth).mean()
    d = k.rolling(d_smooth).mean()
    return k, d


def roc(close: pd.Series, period: int = 9) -> pd.Series:
    """Rate of Change in percent: 100 * (close / close[period ago] - 1)."""
    return 100.0 * (close / close.shift(period) - 1.0)


def heikin_ashi(df: pd.DataFrame):
    """Heikin-Ashi open/high/low/close. HA close = OHLC/4; HA open recurses on the
    prior HA candle (seeded with the first real (open+close)/2)."""
    o = df["open"].to_numpy(); h = df["high"].to_numpy()
    l = df["low"].to_numpy(); c = df["close"].to_numpy()
    n = len(c)
    ha_c = (o + h + l + c) / 4.0
    ha_o = np.empty(n)
    if n:
        ha_o[0] = (o[0] + c[0]) / 2.0
        for i in range(1, n):
            ha_o[i] = (ha_o[i - 1] + ha_c[i - 1]) / 2.0
    ha_h = np.maximum.reduce([h, ha_o, ha_c])
    ha_l = np.minimum.reduce([l, ha_o, ha_c])
    idx = df.index
    return (pd.Series(ha_o, index=idx), pd.Series(ha_h, index=idx),
            pd.Series(ha_l, index=idx), pd.Series(ha_c, index=idx))


# ===================================================================
# Round-3 research indicators (2026-06-04 new-strategy sweep)
# ===================================================================

def gmma(close: pd.Series):
    """Guppy Multiple Moving Average -- two EMA ribbons reduced to their group means.
    Short ribbon = mean of EMA{3,5,8,10,12,15} (trader group); long ribbon = mean of
    EMA{30,35,40,45,50,60} (investor group). The crossover BETWEEN the group means is
    the GMMA trend signal. Returns (short_avg, long_avg)."""
    short_p = (3, 5, 8, 10, 12, 15)
    long_p = (30, 35, 40, 45, 50, 60)
    c = close.to_numpy(dtype=float)
    s = np.mean([_shared.ema(c, p) for p in short_p], axis=0)
    l = np.mean([_shared.ema(c, p) for p in long_p], axis=0)
    return pd.Series(s, index=close.index), pd.Series(l, index=close.index)


def choppiness(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Choppiness Index in [0, 100]; wraps the monorepo-shared numpy port (validated identical to
    the prior pandas form, <3e-14). High (>~61.8) ranging, low (<~38.2) trending."""
    return pd.Series(_shared.choppiness(df["high"].to_numpy(dtype=float), df["low"].to_numpy(dtype=float),
                                        df["close"].to_numpy(dtype=float), period), index=df.index)


def hurst(close: pd.Series, window: int = 100) -> pd.Series:
    """Rolling Hurst exponent (rescaled-range proxy) over `window` bars. For each window of
    log returns: H = log(R/S) / log(N), where R = range of the mean-adjusted cumulative
    deviation and S = std of the returns. H>~0.55 trending (persistent), ~0.50 random walk,
    <~0.45 mean-reverting (anti-persistent). Single-window R/S is a cheap, noisy proxy --
    use a long window / higher timeframe (research flagged the ~100-obs reliability floor)."""
    def _h(x):
        r = np.diff(np.log(x))
        if len(r) < 8:
            return np.nan
        m = r.mean()
        y = np.cumsum(r - m)
        rng = y.max() - y.min()
        s = r.std(ddof=0)
        if s <= 0 or rng <= 0:
            return np.nan
        return np.log(rng / s) / np.log(len(r))
    return close.rolling(window).apply(_h, raw=True)
