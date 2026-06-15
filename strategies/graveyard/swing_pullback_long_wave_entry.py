#!/usr/bin/env python3
"""swing_pullback_long_wave_entry -- Swing pullback to Wave in uptrend: EMA21 rising, price dips to Wave band. thirty_days_of_forex_trading_trades_tactics_and_te.

Uptrend: EMA21 slope rising (close > EMA21 AND EMA21 now > EMA21 N bars ago).
Entry: price pulls back into the Wave band (low <= SMA_HIGH21 from above, i.e. touches the upper band).
The deterministic 'pullback to Wave' variant: price re-touches the SMA21_high envelope during a rising EMA21.
"""
from strategies._common import nan, TREND, ALL_CLASSES

META = {
    "id": "swing_pullback_long_wave_entry",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "trend",
    "tf": "4h",
    "indicators": "close,ema21,sma_high21,sma_low21",
    "long": "EMA21 rising AND close pulls back to touch or enter the Wave band (low <= sma_high21); uptrend pullback entry",
    "short": "EMA21 falling AND close bounces up to touch or enter the Wave band (high >= sma_low21); downtrend bounce-short entry",
    "desc": "Wave pullback/bounce entry: EMA21 slope determines trend; entry when price re-touches the 21-bar high/low MA band",
    "source": "thirty_days_of_forex_trading_trades_tactics_and_te Introduction Figures I.2,I.3",
}


def signal(ind, pos, htf=None):
    """Swing pullback (long) or bounce (short) into the EMA21 Wave band."""
    if pos < 5:
        return None
    c       = ind["close"][pos]
    lo      = ind["low"][pos]
    hi      = ind["high"][pos]
    e21     = ind["ema21"][pos]
    e21_5   = ind["ema21"][pos - 5]
    sh21    = ind["sma_high21"][pos]
    sl21    = ind["sma_low21"][pos]
    if nan(c, lo, hi, e21, e21_5, sh21, sl21):
        return None
    slope_up   = e21 > e21_5
    slope_dn   = e21 < e21_5
    # Long: uptrend slope AND price above the wave but low pulls into upper wave line
    if slope_up and c > sl21 and lo <= sh21:
        return "long"
    # Short: downtrend slope AND price below the wave but high pokes into lower wave line
    if slope_dn and c < sh21 and hi >= sl21:
        return "short"
    return None
