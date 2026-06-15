"""
Single source of truth for the indicator math shared by LAB (backtest) and TRADE (live).

All functions are numpy-array in / numpy-array out (the lowest common denominator): LAB indexes
the returned array by absolute bar `i`, TRADE reads `[-1]`/`[-2]` from the array over a fetched
window. The math here is the clean-room version previously duplicated in TRADE's _common_4h.py +
qqe.py and validated 0-diff vs LAB's backtest indicators.py (see LAB/backtest/validate_indicators.py).

Two EMA variants are deliberately kept distinct (different seed -> different values):
  ema()        SMA seed at [period-1]      -- used for EMA20/EMA200 (ATRC/PSAR/RSI14, LAB ema)
  ema_pandas() first-value seed (ewm)      -- used INSIDE QQE (pandas ewm adjust=False)
"""
from __future__ import annotations

import numpy as np


def ema(x: np.ndarray, period: int) -> np.ndarray:
    """EMA with an SMA seed at index period-1 (the backtest's standard EMA)."""
    n = len(x); out = np.full(n, np.nan)
    if n < period:
        return out
    k = 2.0 / (period + 1.0)
    out[period - 1] = np.mean(x[:period])            # SMA seed
    for i in range(period, n):
        out[i] = x[i] * k + out[i - 1] * (1.0 - k)
    return out


def ema_pandas(x: np.ndarray, span: int) -> np.ndarray:
    """EMA with a first-value seed (pandas ewm adjust=False), alpha=2/(span+1). Used inside QQE."""
    n = len(x); out = np.full(n, np.nan); a = 2.0 / (span + 1.0)
    start = 0
    while start < n and np.isnan(x[start]):
        start += 1
    if start >= n:
        return out
    out[start] = x[start]
    for i in range(start + 1, n):
        out[i] = a * x[i] + (1 - a) * out[i - 1]
    return out


def atr(h: np.ndarray, l: np.ndarray, c: np.ndarray, period: int = 14) -> np.ndarray:
    """Wilder ATR."""
    n = len(c); pc = np.empty(n); pc[0] = np.nan; pc[1:] = c[:-1]
    tr = np.maximum.reduce([h - l, np.abs(h - pc), np.abs(l - pc)]); tr[0] = np.nan
    out = np.full(n, np.nan)
    if 1 + period > n:
        return out
    seed = period
    out[seed] = np.mean(tr[1:1 + period]); prev = out[seed]
    for i in range(1 + period, n):
        prev = (prev * (period - 1) + tr[i]) / period; out[i] = prev
    return out


def wilder_rsi(close: np.ndarray, period: int = 14) -> np.ndarray:
    """Wilder RSI."""
    n = len(close); delta = np.empty(n); delta[0] = np.nan; delta[1:] = np.diff(close)
    gain = np.where(delta > 0, delta, 0.0); loss = np.where(delta < 0, -delta, 0.0)
    gain[0] = np.nan; loss[0] = np.nan

    def wilder(v):
        out = np.full(n, np.nan)
        if 1 + period > n:
            return out
        seed = period; out[seed] = np.mean(v[1:1 + period]); prev = out[seed]
        for i in range(1 + period, n):
            prev = (prev * (period - 1) + v[i]) / period; out[i] = prev
        return out

    ag = wilder(gain); al = wilder(loss)
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = ag / al; out = 100.0 - 100.0 / (1.0 + rs)
    out = np.where(al == 0, 100.0, out)
    out = np.where(np.isnan(ag), np.nan, out)
    return out


def bb(c: np.ndarray, period: int = 20, mult: float = 2.0):
    """Bollinger bands (population std, ddof=0). Returns (mid, upper, lower)."""
    n = len(c); mid = np.full(n, np.nan); up = np.full(n, np.nan); lo = np.full(n, np.nan)
    for i in range(period - 1, n):
        w = c[i - period + 1:i + 1]; m = w.mean(); s = w.std()
        mid[i] = m; up[i] = m + mult * s; lo[i] = m - mult * s
    return mid, up, lo


def bbw_pct(c: np.ndarray, period: int = 20, lookback: int = 120) -> np.ndarray:
    """Bollinger-band-width percentile rank over the lookback window."""
    n = len(c); bbw = np.full(n, np.nan)
    for i in range(period - 1, n):
        w = c[i - period + 1:i + 1]; m = w.mean(); s = w.std()
        if m > 0:
            bbw[i] = (2.0 * s) / m
    out = np.full(n, np.nan)
    for i in range(n):
        if i < lookback - 1:
            continue
        win = bbw[i - lookback + 1:i + 1]
        if np.isnan(win).any():
            continue
        out[i] = 100.0 * (win[-1] > win[:-1]).sum() / max(len(win) - 1, 1)
    return out


def wma(x: np.ndarray, period: int) -> np.ndarray:
    """Weighted moving average."""
    n = len(x); out = np.full(n, np.nan); w = np.arange(1, period + 1); sw = w.sum()
    for i in range(period - 1, n):
        seg = x[i - period + 1:i + 1]
        if np.isnan(seg).any():
            continue
        out[i] = np.dot(seg, w) / sw
    return out


def coppock(c: np.ndarray, r1: int = 14, r2: int = 11, wp: int = 10) -> np.ndarray:
    """Coppock curve: WMA of (ROC(r1) + ROC(r2))."""
    n = len(c); roc = np.full(n, np.nan)
    for i in range(r1, n):
        roc[i] = 100.0 * (c[i] / c[i - r1] - 1.0) + 100.0 * (c[i] / c[i - r2] - 1.0)
    return wma(roc, wp)


def psar_dir(h: np.ndarray, l: np.ndarray, step: float = 0.02, mx: float = 0.2) -> np.ndarray:
    """Parabolic SAR trend direction (+1 up / -1 down)."""
    n = len(h); trend = np.ones(n)
    if n < 2:
        return trend
    up = True; af = step; ep = h[0]; sar = l[0]
    for i in range(1, n):
        prev = sar
        if up:
            cur = prev + af * (ep - prev)
            cur = min(cur, l[i - 1], l[i - 2] if i >= 2 else l[i - 1])
            if l[i] < cur:
                up = False; cur = ep; ep = l[i]; af = step
            elif h[i] > ep:
                ep = h[i]; af = min(af + step, mx)
        else:
            cur = prev + af * (ep - prev)
            cur = max(cur, h[i - 1], h[i - 2] if i >= 2 else h[i - 1])
            if h[i] > cur:
                up = True; cur = ep; ep = h[i]; af = step
            elif l[i] < ep:
                ep = l[i]; af = min(af + step, mx)
        sar = cur; trend[i] = 1 if up else -1
    return trend


def macd(close: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9):
    """MACD line / signal / histogram (arrays). Uses the first-value-seed EMA (ema_pandas),
    matching pandas ewm(adjust=False) for the no-NaN price input."""
    line = ema_pandas(close, fast) - ema_pandas(close, slow)
    sig = ema_pandas(line, signal)
    return line, sig, line - sig


# QQE periods (smoothed-RSI trailing line); FACTOR is the ATR-RSI band multiplier.
QQE_RSI_PERIOD, QQE_SMOOTH, QQE_FACTOR = 14, 5, 4.236


def qqe_values(close: np.ndarray):
    """Return (rsi_ma, qqe_line) arrays."""
    r = wilder_rsi(close, QQE_RSI_PERIOD)
    rsi_ma = ema_pandas(r, QQE_SMOOTH)
    wilder = 2 * QQE_RSI_PERIOD - 1
    atr_rsi = np.abs(np.diff(rsi_ma, prepend=rsi_ma[0]))
    ma_atr_rsi = ema_pandas(atr_rsi, wilder)
    dar = ema_pandas(ma_atr_rsi, wilder) * QQE_FACTOR
    n = len(rsi_ma); line = np.full(n, np.nan)
    for i in range(1, n):
        if np.isnan(rsi_ma[i]) or np.isnan(dar[i]):
            continue
        prev = line[i - 1]
        if np.isnan(prev):
            line[i] = rsi_ma[i] - dar[i] if rsi_ma[i] > 50 else rsi_ma[i] + dar[i]
            continue
        if rsi_ma[i] > prev and rsi_ma[i - 1] > prev:
            line[i] = max(prev, rsi_ma[i] - dar[i])
        elif rsi_ma[i] < prev and rsi_ma[i - 1] < prev:
            line[i] = min(prev, rsi_ma[i] + dar[i])
        elif rsi_ma[i] > prev:
            line[i] = rsi_ma[i] - dar[i]
        else:
            line[i] = rsi_ma[i] + dar[i]
    return rsi_ma, line


def cmo(close: np.ndarray, period: int = 20) -> np.ndarray:
    """Chande Momentum Oscillator in [-100, 100]. Rolling sums of up/down moves over `period`:
    CMO = 100 * (sum_up - sum_down) / (sum_up + sum_down). Direct numpy port of LAB
    indicators.cmo (pandas rolling-sum form). First valid at index `period` (the bar-0 diff is
    NaN, so the first full-window sum lands at `period`). sum_up+sum_down == 0 -> NaN (flat run)."""
    n = len(close)
    out = np.full(n, np.nan)
    delta = np.empty(n); delta[0] = np.nan; delta[1:] = np.diff(close)
    up = np.where(delta > 0, delta, 0.0); dn = np.where(delta < 0, -delta, 0.0)
    up[0] = np.nan; dn[0] = np.nan                       # Edge: bar-0 has no prior close
    for i in range(period, n):
        wu = up[i - period + 1:i + 1]
        if np.isnan(wu).any():                           # window still straddles the NaN seed
            continue
        su = wu.sum(); sd = dn[i - period + 1:i + 1].sum()
        s = su + sd
        if s != 0:                                       # Edge: flat window -> 0/0 stays NaN (LAB parity)
            out[i] = 100.0 * (su - sd) / s
    return out


def chandelier_dir(high: np.ndarray, low: np.ndarray, close: np.ndarray,
                   period: int = 22, mult: float = 3.0) -> np.ndarray:
    """Chandelier Exit direction (+1/-1): close vs the ratcheting long/short stops. Stateful --
    the stop only tightens while price stays on its side, and direction flips when price closes
    through the opposite prior stop. Direct port of LAB indicators.chandelier_dir; the ratchet
    carries across the whole series, so a live caller needs enough warmup bars for the direction
    at the last bar to converge to the full-history value (validated by the signal 0-diff harness)."""
    n = len(close)
    a = atr(high, low, close, period)
    hh = np.full(n, np.nan); ll = np.full(n, np.nan)     # rolling high/low (min_periods=period)
    for i in range(period - 1, n):
        hh[i] = high[i - period + 1:i + 1].max()
        ll[i] = low[i - period + 1:i + 1].min()
    long_stop = np.full(n, np.nan); short_stop = np.full(n, np.nan)
    direction = np.zeros(n); prev = 1.0
    for i in range(n):
        if np.isnan(a[i]):                               # warmup: ATR not seeded yet
            continue
        ls = hh[i] - mult * a[i]; ss = ll[i] + mult * a[i]
        if i > 0 and not np.isnan(long_stop[i - 1]):
            ls = max(ls, long_stop[i - 1]) if close[i - 1] > long_stop[i - 1] else ls
            ss = min(ss, short_stop[i - 1]) if close[i - 1] < short_stop[i - 1] else ss
        long_stop[i] = ls; short_stop[i] = ss
        if close[i] > (short_stop[i - 1] if i > 0 and not np.isnan(short_stop[i - 1]) else ss):
            prev = 1.0
        elif close[i] < (long_stop[i - 1] if i > 0 and not np.isnan(long_stop[i - 1]) else ls):
            prev = -1.0
        direction[i] = prev
    return direction


def choppiness(h: np.ndarray, l: np.ndarray, c: np.ndarray, period: int = 14) -> np.ndarray:
    """Choppiness Index in [0, 100]. CHOP = 100 * log10(sum(TR, n) / (maxHigh(n) - minLow(n)))
    / log10(n). High (>~61.8) = choppy/ranging, low (<~38.2) = trending. Direction-independent.
    Direct numpy port of LAB indicators.choppiness (pandas rolling form): TR[0] is NaN (no prior
    close), so the first full-window value lands at index `period` (window straddling the seed
    stays NaN, matching pandas min_periods)."""
    n = len(c)
    out = np.full(n, np.nan)
    pc = np.empty(n); pc[0] = np.nan; pc[1:] = c[:-1]
    tr = np.maximum.reduce([h - l, np.abs(h - pc), np.abs(l - pc)]); tr[0] = np.nan
    for i in range(period, n):
        wtr = tr[i - period + 1:i + 1]
        if np.isnan(wtr).any():                          # window still straddles the NaN seed
            continue
        s = wtr.sum()
        rng = h[i - period + 1:i + 1].max() - l[i - period + 1:i + 1].min()
        if rng > 0:                                      # Edge: flat window -> stays NaN (safe)
            out[i] = 100.0 * np.log10(s / rng) / np.log10(period)
    return out
