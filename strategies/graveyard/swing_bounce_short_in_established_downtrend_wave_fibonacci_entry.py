#!/usr/bin/env python3
"""swing_bounce_short_in_established_downtrend_wave_fibonacci_entry -- Swing bounce to Wave in downtrend: EMA21 falling, high pokes into Wave band. thirty_days_of_forex_trading_trades_tactics_and_te.

Downtrend: EMA21 slope falling over 5 bars.
Entry: price bounces up into the Wave band from below (high >= sma_low21 while close still below sma_high21).
Deterministic 'bounce to Wave' variant: price re-touches the lower Wave lines while trend is down.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "swing_bounce_short_in_established_downtrend_wave_fibonacci_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,ema21,sma_high21,sma_low21",
    "long": None,
    "short": "EMA21 falling (downtrend) AND high bounces up to touch the lower Wave band (sma_low21)",
    "desc": "Wave bounce short: EMA21 slope falling; entry when price bounces into the 21-bar low MA band",
    "source": "thirty_days_of_forex_trading_trades_tactics_and_te Introduction Figures I.3 I.11",
}


def signal(ind, pos, htf=None):
    """Swing bounce into Wave band during EMA21 downtrend."""
    if pos < 5:
        return None
    c    = ind["close"][pos]
    hi   = ind["high"][pos]
    e21  = ind["ema21"][pos]
    e21p = ind["ema21"][pos - 5]
    sh21 = ind["sma_high21"][pos]
    sl21 = ind["sma_low21"][pos]
    if nan(c, hi, e21, e21p, sh21, sl21):
        return None
    slope_dn = e21 < e21p
    # Only shorts in downtrend: price below upper Wave but high pokes into lower Wave band
    if slope_dn and c < sh21 and hi >= sl21:
        return "short"
    return None
