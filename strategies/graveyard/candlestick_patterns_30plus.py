#!/usr/bin/env python3
"""candlestick_patterns_30plus -- 30+ candlestick pattern basket. hasnocool Pine script.

Detects a curated set of bullish and bearish candlestick patterns from OHLC math.
Bullish: Hammer, Morning Star (3-candle), Piercing, Bullish Engulfing, Bullish Harami, Inverted Hammer.
Bearish: Hanging Man, Evening Star (3-candle), Dark Cloud Cover, Bearish Engulfing, Bearish Harami, Shooting Star.
Uses ha_close/ha_open for trend context (Heikin-Ashi smoothed context for pattern validation).
"""
from strategies._common import nan, REVERT, ALL_CLASSES

META = {
    "id": "candlestick_patterns_30plus",
    "cadences": ["day", "swing"],
    "exit": REVERT,
    "asset_classes": ALL_CLASSES,
    "style": "revert",
    "tf": "4h",
    "indicators": "open, high, low, close, ha_open, ha_close",
    "long": "bullish pattern detected: Hammer, Morning Star, Piercing, Engulfing, Harami, Inv Hammer",
    "short": "bearish pattern detected: Hanging Man, Evening Star, Dark Cloud, Engulfing, Harami, Shooting Star",
    "desc": "Candlestick pattern basket: bullish or bearish pattern vote from OHLC-only math",
    "source": "web:https://github.com/hasnocool/tradingview-pine-scripts/blob/main/All%20Candlestick%20Patterns%20Strategy.pine",
}


def signal(ind, pos, htf=None):
    """Pattern basket: any bullish = long, any bearish = short."""
    if pos < 2:
        return None
    c = ind["close"][pos]
    o = ind["open"][pos]
    h = ind["high"][pos]
    lo = ind["low"][pos]
    c1 = ind["close"][pos - 1]
    o1 = ind["open"][pos - 1]
    h1 = ind["high"][pos - 1]
    lo1 = ind["low"][pos - 1]
    c2 = ind["close"][pos - 2]
    o2 = ind["open"][pos - 2]
    ha_c = ind["ha_close"][pos]
    ha_o = ind["ha_open"][pos]
    if nan(c, o, h, lo, c1, o1, h1, lo1, c2, o2, ha_c, ha_o):
        return None

    body = abs(c - o)
    body1 = abs(c1 - o1)
    rng = h - lo if h != lo else 1e-10
    rng1 = h1 - lo1 if h1 != lo1 else 1e-10

    # Helper direction checks
    bear_prior = c1 < o1
    bull_prior = c1 > o1
    bull_cur = c > o
    bear_cur = c < o

    # --- Bullish patterns ---
    # Hammer: small body (< 30% range), long lower shadow (> 2x body), little upper shadow
    lower_shadow = min(c, o) - lo
    upper_shadow = h - max(c, o)
    hammer = (body < rng * 0.3) and (lower_shadow > body * 2) and (upper_shadow < body * 0.5) and bear_prior

    # Inverted Hammer: small body, long upper shadow, in downtrend
    inv_hammer = (body < rng * 0.3) and (upper_shadow > body * 2) and (lower_shadow < body * 0.5) and bear_prior

    # Bullish Engulfing: prior bearish, current bullish, current body engulfs prior
    bull_engulf = bear_prior and bull_cur and o < c1 and c > o1

    # Bullish Harami: prior bearish (large body), current bullish (small body inside prior)
    bull_harami = bear_prior and bull_cur and c < o1 and o > c1 and body < body1 * 0.5

    # Piercing: prior bearish, current bullish, closes above midpoint of prior body
    mid_bear1 = (o1 + c1) / 2.0
    piercing = bear_prior and bull_cur and o < c1 and c > mid_bear1 and c < o1

    # Morning Star (3-candle): candle[2] bearish, candle[1] doji/small, candle[0] bullish above midpoint
    bear2 = c2 < o2
    doji1 = body1 < abs(c2 - o2) * 0.25
    mid_bear2 = (o2 + c2) / 2.0
    morning_star = bear2 and doji1 and bull_cur and c > mid_bear2

    bull_signal = hammer or inv_hammer or bull_engulf or bull_harami or piercing or morning_star

    # --- Bearish patterns ---
    lower_shadow1 = min(c1, o1) - lo1
    upper_shadow1 = h1 - max(c1, o1)

    # Hanging Man: same shape as Hammer but after uptrend (ha_close-based trend context)
    uptrend = ha_c > ha_o
    hanging_man = (body < rng * 0.3) and (lower_shadow > body * 2) and (upper_shadow < body * 0.5) and uptrend

    # Shooting Star: small body, long upper shadow, after uptrend
    shooting_star = (body < rng * 0.3) and (upper_shadow > body * 2) and (lower_shadow < body * 0.5) and uptrend

    # Bearish Engulfing: prior bullish, current bearish, current body engulfs prior
    bear_engulf = bull_prior and bear_cur and o > c1 and c < o1

    # Bearish Harami: prior bullish (large), current bearish (small inside prior)
    bear_harami = bull_prior and bear_cur and c > o1 and o < c1 and body < body1 * 0.5

    # Dark Cloud Cover: prior bullish, current bearish, opens above prior high, closes below midpoint
    mid_bull1 = (o1 + c1) / 2.0
    dark_cloud = bull_prior and bear_cur and o > h1 and c < mid_bull1 and c > o1

    # Evening Star (3-candle): candle[2] bullish, candle[1] doji/small, candle[0] bearish
    bull2 = c2 > o2
    doji1b = body1 < abs(c2 - o2) * 0.25
    mid_bull2 = (o2 + c2) / 2.0
    evening_star = bull2 and doji1b and bear_cur and c < mid_bull2

    bear_signal = hanging_man or shooting_star or bear_engulf or bear_harami or dark_cloud or evening_star

    if bull_signal and not bear_signal:
        return "long"
    if bear_signal and not bull_signal:
        return "short"
    return None
