#!/usr/bin/env python3
"""macd_histogram_three_bar_pattern -- MACD histogram 3-bar exhaustion reversal. quivofx.

Three consecutive histogram bars same sign, then a reversal bar signals momentum exhaustion.
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "macd_histogram_three_bar_pattern",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "reversal",
    "tf": "4h",
    "indicators": "macd_hist",
    "long": "Three consecutive negative histogram bars each more negative, then histogram turns up",
    "short": "Three consecutive positive histogram bars each more positive, then histogram turns down",
    "desc": "MACD histogram three-bar exhaustion reversal pattern",
    "source": "https://quivofx.com/expert-advisor/macd-ea/",
}


def signal(ind, pos, htf=None):
    """MACD histogram three-bar pattern: three same-sign bars then reversal."""
    h0 = ind["macd_hist"][pos]
    h1 = ind["macd_hist"][pos - 1]
    h2 = ind["macd_hist"][pos - 2]
    h3 = ind["macd_hist"][pos - 3]
    if nan(h0, h1, h2, h3):
        return None
    # Long: three red (negative, each more negative) then current bar turns up
    if h1 < 0 and h2 < 0 and h3 < 0 and h1 < h2 and h2 < h3 and h0 > h1:
        return "long"
    # Short: three blue (positive, each more positive) then current bar turns down
    if h1 > 0 and h2 > 0 and h3 > 0 and h1 > h2 and h2 > h3 and h0 < h1:
        return "short"
    return None
