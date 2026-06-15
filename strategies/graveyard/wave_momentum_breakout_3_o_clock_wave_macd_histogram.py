#!/usr/bin/env python3
"""wave_momentum_breakout_macd -- Raghee Wave breakout: flat EMA channel + MACD histogram confirmation. thirty_days_of_forex_trading_trades_tactics_and_te.

Wave flat (3 o'clock): EMA21 slope near zero (ATR-normalised slope small).
Long: price (close) breaks ABOVE the upper Wave band (sma_high21) AND MACD histogram > 0.
Short: price breaks BELOW the lower Wave band (sma_low21) AND MACD histogram < 0.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "wave_momentum_breakout_3_o_clock_wave_macd_histogram",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "4h",
    "indicators": "close,ema21,sma_high21,sma_low21,macd_hist,atr",
    "long": "EMA21 slope near zero (consolidation) AND close breaks above sma_high21 AND MACD hist > 0",
    "short": "EMA21 flat AND close breaks below sma_low21 AND MACD hist < 0",
    "desc": "Raghee Wave momentum breakout: flat EMA21 channel breakout confirmed by positive MACD histogram",
    "source": "thirty_days_of_forex_trading_trades_tactics_and_te Days 1-18 esp Day3 p169-173",
}


def signal(ind, pos, htf=None):
    """Wave flat breakout with MACD histogram confirmation."""
    if pos < 6:
        return None
    c    = ind["close"][pos]
    c1   = ind["close"][pos - 1]
    e    = ind["ema21"][pos]
    e5   = ind["ema21"][pos - 5]
    sh21 = ind["sma_high21"][pos]
    sl21 = ind["sma_low21"][pos]
    mh   = ind["macd_hist"][pos]
    a    = ind["atr"][pos]
    if nan(c, c1, e, e5, sh21, sl21, mh, a) or a == 0:
        return None
    slope = abs((e - e5) / a)
    flat  = slope < 0.08    # ATR-normalised near-zero slope = 3 o'clock
    if not flat:
        return None
    if c > sh21 and c1 <= sh21 and mh > 0:
        return "long"
    if c < sl21 and c1 >= sl21 and mh < 0:
        return "short"
    return None
