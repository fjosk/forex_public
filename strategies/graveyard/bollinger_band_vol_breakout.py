#!/usr/bin/env python3
"""bollinger_band_vol_breakout -- Bollinger Band volatility breakout: after a squeeze (very narrow bands), a close outside the upper or lower band signals an explosive directional move. Elder Section 45.

Price/OHLC only. No volume.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "bollinger_band_vol_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1h-4h",
    "indicators": "bb_up, bb_lo, bb_width, bbw_pct, close",
    "long": "bbw_pct below squeeze threshold (25th pctile) and close breaks above upper band",
    "short": "bbw_pct below squeeze threshold and close breaks below lower band",
    "desc": "Bollinger Band volatility breakout after a squeeze: low bbw_pct followed by close outside the band",
    "source": "elder_alexander_trading_for_a_living -- Section 45 Standard Deviation Channels / Bollinger Bands p.251-253",
}

# bbw_pct near zero means the band is compressed relative to recent history;
# threshold 25 = bottom quarter of the bbw_pct range (squeeze)
_SQUEEZE_PCT = 25.0


def signal(ind, pos, htf=None):
    """Squeeze then breakout: bbw_pct low and close outside band."""
    c = ind["close"][pos]
    bu = ind["bb_up"][pos]
    bl = ind["bb_lo"][pos]
    bwp = ind["bbw_pct"][pos]
    if nan(c, bu, bl, bwp):
        return None
    if bwp > _SQUEEZE_PCT:
        return None  # not a squeeze, skip
    if c > bu:
        return "long"
    if c < bl:
        return "short"
    return None
