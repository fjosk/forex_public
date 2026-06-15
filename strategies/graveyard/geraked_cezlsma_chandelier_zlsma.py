#!/usr/bin/env python3
"""geraked_cezlsma_chandelier_zlsma -- Chandelier Exit direction + HMA21 slope on Heikin-Ashi. geraked."""
from strategies._common import nan, TREND, ALL_CLASSES

# ZLSMA not available; hma21 (Hull MA) is the closest zero-lag proxy.
# chand_dir available directly.

META = {
    "id": "geraked_cezlsma_chandelier_zlsma",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "1h",
    "indicators": "chand_dir, hma21, ha_close, ha_open",
    "long": "chand_dir turns long AND hma21 slope turns positive (ZLSMA proxy)",
    "short": "chand_dir turns short AND hma21 slope turns negative",
    "desc": "Chandelier Exit direction + HMA21 slope (ZLSMA proxy) on Heikin-Ashi candles",
    "source": "https://github.com/geraked/metatrader5",
}


def signal(ind, pos, htf=None):
    """Chandelier direction flip confirmed by HMA21 slope."""
    cd = ind["chand_dir"][pos]
    cd1 = ind["chand_dir"][pos - 1]
    h21 = ind["hma21"][pos]
    h21_1 = ind["hma21"][pos - 1]
    ha_c = ind["ha_close"][pos]
    ha_o = ind["ha_open"][pos]
    if nan(cd, cd1, h21, h21_1, ha_c, ha_o):
        return None
    ce_turns_long = cd == 1 and cd1 != 1
    ce_turns_short = cd == -1 and cd1 != -1
    hma_bull = h21 > h21_1
    hma_bear = h21 < h21_1
    if ce_turns_long and hma_bull:
        return "long"
    if ce_turns_short and hma_bear:
        return "short"
    return None
