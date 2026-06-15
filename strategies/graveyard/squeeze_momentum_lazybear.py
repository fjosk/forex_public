#!/usr/bin/env python3
"""squeeze_momentum_lazybear -- BB inside KC squeeze detection with MACD histogram direction. LazyBear."""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "squeeze_momentum_lazybear",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "momentum",
    "tf": "1h/4h/daily",
    "indicators": "bb_lo, bb_up, kc_lo, kc_up, macd_hist, ema200",
    "long": "squeeze releases (BB exits KC) AND macd_hist positive and rising AND close above ema200",
    "short": "squeeze releases AND macd_hist negative and falling AND close below ema200",
    "desc": "TTM Squeeze / LazyBear: BB-inside-KC squeeze release with momentum direction",
    "source": "web:https://www.tradingview.com/script/nqQ1DT5a-Squeeze-Momentum-Indicator-LazyBear/",
}


def signal(ind, pos, htf=None):
    """Squeeze release breakout: BB exits KC while momentum (macd_hist proxy) confirms direction."""
    if pos < 1:
        return None
    bb_lo = ind["bb_lo"][pos]
    bb_up = ind["bb_up"][pos]
    kc_lo = ind["kc_lo"][pos]
    kc_up = ind["kc_up"][pos]
    mh0 = ind["macd_hist"][pos]
    mh1 = ind["macd_hist"][pos - 1]
    c = ind["close"][pos]
    e200 = ind["ema200"][pos]
    if nan(bb_lo, bb_up, kc_lo, kc_up, mh0, mh1, c, e200):
        return None

    # Squeeze is OFF when BB is outside KC (bands have expanded beyond KC)
    squeeze_off = not (bb_lo > kc_lo and bb_up < kc_up)

    if squeeze_off and mh0 > 0 and mh0 > mh1 and c > e200:
        return "long"
    if squeeze_off and mh0 < 0 and mh0 < mh1 and c < e200:
        return "short"

    return None
