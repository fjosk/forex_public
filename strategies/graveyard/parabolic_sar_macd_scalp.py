#!/usr/bin/env python3
"""parabolic_sar_macd_scalp -- PSAR flip + MACD hist + EMA50 trend filter scalp. web:forexfactory.com."""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "parabolic_sar_macd_scalp",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "psar_dir, macd_hist, ema50 (proxy ema100)",
    "long": "close > ema50 AND macd_hist > 0 AND psar_dir flips to +1",
    "short": "close < ema50 AND macd_hist < 0 AND psar_dir flips to -1",
    "desc": "PSAR direction flip entry confirmed by MACD histogram and EMA50 trend filter",
    "source": "web:https://www.forexfactory.com/thread/1140508-parabolic-sar-trend-scalper-trading-system",
}


def signal(ind, pos, htf=None):
    """PSAR flips direction; MACD histogram and EMA50 must agree for trade entry."""
    pdir = ind["psar_dir"][pos]
    pdir_p = ind["psar_dir"][pos - 1]
    mh = ind["macd_hist"][pos]
    e50 = ind["ema50"][pos]
    c = ind["close"][pos]
    if nan(pdir, pdir_p, mh, e50, c):
        return None
    psar_flip_bull = pdir > 0 and pdir_p <= 0
    psar_flip_bear = pdir < 0 and pdir_p >= 0
    if psar_flip_bull and mh > 0 and c > e50:
        return "long"
    if psar_flip_bear and mh < 0 and c < e50:
        return "short"
    return None
