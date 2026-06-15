#!/usr/bin/env python3
"""trade_day_of_week_tdw_volatility_breakout -- Daily range breakout filtered by day-of-week:
buy only on Tue/Thu, sell only on Wed/Thu (bond-market optimal days per the research).
long_term_secrets_to_short_term_trading Ch.4.

Breakout: close > prev_dhh (prior day high) for a long; close < prev_dll (prior day low) for
a short. Day-of-week filter gates which signals are taken.
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "trade_day_of_week_tdw_volatility_breakout",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d",
    "indicators": "dow,close,prev_dhh,prev_dll",
    "long": "close > prior-day high AND today is Tuesday or Thursday (best buy days)",
    "short": "close < prior-day low AND today is Wednesday or Thursday (best sell days)",
    "desc": "TDW-filtered volatility breakout: take daily range breaks only on historically best weekdays",
    "source": "long_term_secrets_to_short_term_trading Ch.4 Simple Daily Range Breakouts pp.61-71 Figures 4.2-4.18",
}

# Python weekday: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri
_BUY_DAYS  = {1, 3}   # Tuesday, Thursday
_SELL_DAYS = {2, 3}   # Wednesday, Thursday


def signal(ind, pos, htf=None):
    """Range breakout gated by best weekday for each direction."""
    if pos < 1:
        return None
    dw   = ind["dow"][pos]
    c    = ind["close"][pos]
    phh  = ind["prev_dhh"][pos]
    pll  = ind["prev_dll"][pos]
    if nan(dw, c, phh, pll):
        return None
    wd = int(dw)
    if wd in _BUY_DAYS and c > phh:
        return "long"
    if wd in _SELL_DAYS and c < pll:
        return "short"
    return None
