#!/usr/bin/env python3
"""dual_supertrend_macd -- Dual Supertrend + MACD Confirmation (presentTrading).
web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/Dual-Supertrend%20with%20MACD%20-%20Strategy%20%5BpresentTrading%5D.pine
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "dual_supertrend_macd",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "swing",
    "tf": "4h",
    "indicators": "st_dir, st_dir_fast, macd_hist",
    "long": "st_dir < 0 AND st_dir_fast < 0 AND macd_hist > 0 (both STs bullish + MACD positive)",
    "short": "st_dir > 0 AND st_dir_fast > 0 AND macd_hist < 0",
    "desc": "Both Supertrend instances agree on direction AND MACD histogram confirms; tight AND entry",
    "source": "web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/Dual-Supertrend%20with%20MACD%20-%20Strategy%20%5BpresentTrading%5D.pine",
}


def signal(ind, pos, htf=None):
    """Dual Supertrend agreement with MACD histogram sign confirmation."""
    std = ind["st_dir"][pos]
    stf = ind["st_dir_fast"][pos]
    mh = ind["macd_hist"][pos]
    if nan(std, stf, mh):
        return None
    if std < 0 and stf < 0 and mh > 0:
        return "long"
    if std > 0 and stf > 0 and mh < 0:
        return "short"
    return None
