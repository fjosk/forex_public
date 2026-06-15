#!/usr/bin/env python3
"""channel_breakout_retest_continuation -- Price blows beyond EMA channel then retraces to EMA; re-enter in EMA slope direction. come_into_my_trading_room_elder."""
from strategies._common import nan, _xup, _xdn, TREND, ALL_CLASSES

META = {
    "id": "channel_breakout_retest_continuation",
    "cadences": ["day", "swing"],
    "exit": TREND,
    "asset_classes": ALL_CLASSES,
    "style": "breakout",
    "tf": "1d-4h",
    "indicators": "ema20, bb_up, bb_lo, close, low, high",
    "long": "price previously exceeded bb_up then pulled back to ema20 in uptrend; enter long with EMA slope up",
    "short": "price previously exceeded bb_lo then retraced to ema20 in downtrend; enter short with EMA slope down",
    "desc": "Channel blowout-retest continuation: breakout beyond Bollinger band, retest EMA, re-enter in EMA direction",
    "source": "come_into_my_trading_room_alexander_elder",
}


def signal(ind, pos, htf=None):
    """Blowout beyond Bollinger band then retest of EMA in EMA slope direction."""
    if pos < 3:
        return None
    c = ind["close"]
    h = ind["high"]
    l = ind["low"]
    ema = ind["ema20"]
    bb_up = ind["bb_up"]
    bb_lo = ind["bb_lo"]

    cv = c[pos]
    hv = h[pos]
    lv = l[pos]
    ev = ema[pos]
    ev1 = ema[pos - 1]

    if nan(cv, hv, lv, ev, ev1, bb_up[pos - 1], bb_up[pos - 2], bb_lo[pos - 1], bb_lo[pos - 2]):
        return None

    # EMA slope
    ema_up = ev > ev1
    ema_dn = ev < ev1

    # Check if within last 3 bars price exceeded the band (blowout)
    blew_up = any(h[pos - k] > bb_up[pos - k] for k in range(1, 3) if not nan(h[pos - k], bb_up[pos - k]))
    blew_dn = any(l[pos - k] < bb_lo[pos - k] for k in range(1, 3) if not nan(l[pos - k], bb_lo[pos - k]))

    # Current bar has returned to near the EMA (within 0.5 ATR proxy: use bb half-width / 4)
    bb_half = (bb_up[pos] - bb_lo[pos]) / 4.0 if not nan(bb_up[pos], bb_lo[pos]) else 0
    near_ema_long = lv <= ev + bb_half and hv >= ev - bb_half
    near_ema_short = hv >= ev - bb_half and lv <= ev + bb_half

    if blew_up and ema_up and near_ema_long and cv > ev:
        return "long"
    if blew_dn and ema_dn and near_ema_short and cv < ev:
        return "short"
    return None
