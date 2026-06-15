#!/usr/bin/env python3
"""order_block_entry -- ICT Order Block Entry. ICT / SMC community.

The last opposing candle before a sharp impulsive displacement (>2 ATR in next 3 bars).
Price retraces back into that candle's body zone; entry taken on the retrace bar.
Source: web:https://www.mindmathmoney.com/articles/order-block-trading-strategy-a-complete-guide-to-smart-money-concepts-2025
"""
from strategies._common import nan, BREAK, ALL_CLASSES

META = {
    "id": "order_block_entry",
    "cadences": ["day", "swing"],
    "exit": BREAK,
    "asset_classes": ALL_CLASSES,
    "style": "day",
    "tf": "1h",
    "indicators": "close, open, high, low, atr, frac_up_px, frac_dn_px",
    "long": "last bearish candle before 3-bar bull displacement >2 ATR; price retraces into body zone [ob_lo, ob_hi]",
    "short": "last bullish candle before 3-bar bear displacement >2 ATR; price retraces into body zone",
    "desc": "ICT Order Block: retrace into the last opposing candle before a displacement impulse",
    "source": "web:https://www.mindmathmoney.com/articles/order-block-trading-strategy-a-complete-guide-to-smart-money-concepts-2025",
}

_LOOKBACK = 10    # bars to scan back for an OB candidate
_DISP_BARS = 3    # bars after OB to confirm displacement
_DISP_ATR = 2.0   # displacement size in ATR multiples


def signal(ind, pos, htf=None):
    """Order block: scan recent bars for last opposing candle before a displacement; trade retrace."""
    if pos < _LOOKBACK + _DISP_BARS + 1:
        return None

    closes = ind["close"]
    opens = ind["open"]
    highs = ind["high"]
    lows = ind["low"]
    atrs = ind["atr"]

    c = closes[pos]
    lo = lows[pos]
    hi = highs[pos]
    atr_cur = atrs[pos]
    if nan(c, lo, hi, atr_cur) or atr_cur == 0:
        return None

    # Scan back for a bullish OB (last bearish candle before bullish displacement)
    for k in range(1, _LOOKBACK + 1):
        ob_pos = pos - k
        if ob_pos < _DISP_BARS:
            break
        ob_o = opens[ob_pos]
        ob_c = closes[ob_pos]
        ob_lo = lows[ob_pos]
        if nan(ob_o, ob_c, ob_lo):
            continue
        # OB candidate: bearish candle
        if ob_c >= ob_o:
            continue
        # Check displacement in next _DISP_BARS bars
        disp_end = ob_pos + _DISP_BARS
        if disp_end >= pos:
            continue
        net_move = closes[disp_end] - ob_c
        atr_ob = atrs[ob_pos]
        if nan(atr_ob) or atr_ob == 0:
            continue
        if net_move >= _DISP_ATR * atr_ob:
            # Bullish OB confirmed; retrace zone = [ob_lo, ob_o]
            ob_hi_zone = ob_o
            if lo <= ob_hi_zone and c >= ob_lo:
                return "long"
            break  # found the most recent OB; stop scanning

    # Scan back for a bearish OB (last bullish candle before bearish displacement)
    for k in range(1, _LOOKBACK + 1):
        ob_pos = pos - k
        if ob_pos < _DISP_BARS:
            break
        ob_o = opens[ob_pos]
        ob_c = closes[ob_pos]
        ob_hi = highs[ob_pos]
        if nan(ob_o, ob_c, ob_hi):
            continue
        # OB candidate: bullish candle
        if ob_c <= ob_o:
            continue
        disp_end = ob_pos + _DISP_BARS
        if disp_end >= pos:
            continue
        net_move = ob_c - closes[disp_end]
        atr_ob = atrs[ob_pos]
        if nan(atr_ob) or atr_ob == 0:
            continue
        if net_move >= _DISP_ATR * atr_ob:
            # Bearish OB confirmed; retrace zone = [ob_c, ob_hi]
            ob_lo_zone = ob_c
            if hi >= ob_lo_zone and c <= ob_hi:
                return "short"
            break

    return None
