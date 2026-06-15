#!/usr/bin/env python3
"""triple_sma_4_9_18_crossover -- Triple SMA 4/9/18 crossover swing. web:babypips.com.

Three SMAs (close_sma5 ~ 4-period, sma10 ~ 9-period, sma20 ~ 18-period) must align and
the fast crosses the medium. Exact 4/9/18 not available; closest proxies used as spec documents.
No volume dependency.
"""
from strategies._common import nan, TREND_FLIP, ALL_CLASSES

META = {
    "id": "triple_sma_4_9_18_crossover",
    "cadences": ["day", "swing"],
    "exit": TREND_FLIP,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "daily",
    "indicators": "close_sma5 (proxy 4), sma10 (proxy 9), sma20 (proxy 18)",
    "long": "close_sma5 crosses above sma10 AND both above sma20 (fresh bullish stack)",
    "short": "close_sma5 crosses below sma10 AND both below sma20 (fresh bearish stack)",
    "desc": "Triple SMA 4-9-18 crossover with perfect-stack confirmation (proxied by 5/10/20)",
    "source": "web:https://www.babypips.com/trading/forex-triple-sma-crossover-20141010",
}


def signal(ind, pos, htf=None):
    """Three SMA perfect-stack entry with fast/medium crossover."""
    s5, s5p = ind["close_sma5"][pos], ind["close_sma5"][pos - 1]
    s10, s10p = ind["sma10"][pos], ind["sma10"][pos - 1]
    s20 = ind["sma20"][pos]
    if nan(s5, s5p, s10, s10p, s20):
        return None
    # fresh cross: fast was below medium last bar, now above
    cross_up = s5 > s10 and s5p <= s10p
    cross_dn = s5 < s10 and s5p >= s10p
    if cross_up and s5 > s20 and s10 > s20:
        return "long"
    if cross_dn and s5 < s20 and s10 < s20:
        return "short"
    return None
