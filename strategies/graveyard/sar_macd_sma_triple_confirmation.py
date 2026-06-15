#!/usr/bin/env python3
"""sar_macd_sma_triple_confirmation -- PSAR + MACD histogram + SMA50 three-way confirmation. MQL4."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "sar_macd_sma_triple_confirmation",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "macd_hist, psar_dir, sma50, close",
    "long": "macd_hist > 0 AND psar_dir == +1 AND close > sma50",
    "short": "macd_hist < 0 AND psar_dir == -1 AND close < sma50",
    "desc": "Triple confirmation: MACD histogram + PSAR direction + price vs SMA50 all agree",
    "source": "SAR_MACD_EA (MQL4 Code Base); SMA40 approximated by SMA50",
}


def signal(ind, pos, htf=None):
    """All three conditions must agree for a signal."""
    mh = ind["macd_hist"][pos]
    pd = ind["psar_dir"][pos]
    s50 = ind["sma50"][pos]
    c = ind["close"][pos]
    if nan(mh, pd, s50, c):
        return None
    if mh > 0 and pd > 0 and c > s50:
        return "long"
    if mh < 0 and pd < 0 and c < s50:
        return "short"
    return None
