#!/usr/bin/env python3
"""macd_psar_ema200 -- MACD hist zero-cross + PSAR direction + EMA200 trend. daviddtech.medium.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "macd_psar_ema200",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "macd_hist, psar_dir, ema200",
    "long": "macd_hist crosses above 0 AND psar_dir == 1 (SAR below price) AND close > ema200",
    "short": "macd_hist crosses below 0 AND psar_dir == -1 AND close < ema200",
    "desc": "Triple-filter: MACD histogram zero-cross + Parabolic SAR direction + EMA200 trend",
    "source": "web:https://daviddtech.medium.com/70-win-rate-highly-profitable-macd-parabolic-sar-200-ema-trading-strategy-8f49f8503aa",
}


def signal(ind, pos, htf=None):
    """MACD histogram zero-cross + psar_dir + ema200 all agree."""
    mh = ind["macd_hist"][pos]
    mhp = ind["macd_hist"][pos - 1]
    pd = ind["psar_dir"][pos]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(mh, mhp, pd, c, e200):
        return None
    macd_up = mh > 0 and mhp <= 0
    macd_dn = mh < 0 and mhp >= 0
    if macd_up and pd == 1 and c > e200:
        return "long"
    if macd_dn and pd == -1 and c < e200:
        return "short"
    return None
