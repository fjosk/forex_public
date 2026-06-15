#!/usr/bin/env python3
"""psar_macd_sma220_5m -- PSAR direction + SMA200 baseline + MACD histogram direction. web:strategy-workspaceegiesresources.com."""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "psar_macd_sma220_5m",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "scalp",
    "tf": "5m",
    "indicators": "psar_dir, sma200 (proxy sma220), macd_hist",
    "long": "psar_dir > 0 AND close > sma200 AND macd_hist > 0",
    "short": "psar_dir < 0 AND close < sma200 AND macd_hist < 0",
    "desc": "PSAR + SMA200 baseline + MACD histogram three-condition 5m scalp",
    "source": "web:https://www.strategy-workspaceegiesresources.com/scalping-forex-strategies-ii/184-5-min-scalping-with-parabolic-sar-and-macd/",
}


def signal(ind, pos, htf=None):
    """PSAR direction, SMA200 trend filter, and MACD histogram all must agree."""
    pdir = ind["psar_dir"][pos]
    s200 = ind["sma200"][pos]
    mh = ind["macd_hist"][pos]
    c = ind["close"][pos]
    if nan(pdir, s200, mh, c):
        return None
    if pdir > 0 and c > s200 and mh > 0:
        return "long"
    if pdir < 0 and c < s200 and mh < 0:
        return "short"
    return None
