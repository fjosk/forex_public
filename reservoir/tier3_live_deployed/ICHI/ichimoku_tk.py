from __future__ import annotations

"""
ICHI -- Ichimoku Tenkan/Kijun cross (the strongest edge from the sister-lab/backtest
research sweep, 2026-05-31). Plugged 2026-05-31 to local paper + testnet alongside B1.

SIGNAL TIMEFRAME IS 4h. The strategy was validated at the "swing" cadence (4h entry,
1h/finer exits). TRADE runs the roster on a 1h interval, so this builder reads the
`candles_4h` argument (which the runners fetch and pass) for its entry signal, NOT the
1h `candles`. Running it on 1h is the wrong, money-losing cadence -- do not.

WHY THIS ONE. Across all 13 coins, full unified history, realistic Hyperliquid fees
(4.5 bps/side), this was the only strategy with a BROAD portfolio edge rather than a
single-coin fluke: at 4h, profit factor 1.157, 11/13 coins net positive, qualifiers
SOL/NEAR/TON/SUI (win 56-60%). Scoped to those 4 qualifiers here via
cfg['strategy_universe']['ICHI'] (set in paper_trader.DEFAULT_CONFIG).

CAVEAT: in-sample, full-history backtest, no walk-forward split -- same status as B1.
This is a paper/testnet forward-test, NOT a proven live edge.

Entry (decided on the just-closed 4h candle):
  long  : Tenkan crosses ABOVE Kijun AND close is ABOVE the cloud (max of span A/B)
  short : Tenkan crosses BELOW Kijun AND close is BELOW the cloud (min of span A/B)
Cloud spans are decision-time aligned (the span under the current bar is built from the
bar 26 back -- no look-ahead).

Exit params ride on the signal (the backtest TREND archetype): ATR stop 2.0x, ATR
target 4.0x, no S/R cap, no min-R:R gate. The shared core adds Chandelier trailing
(after +1R) and the time stop. ATR is taken from the 4h candles (the entry timeframe),
matching the backtest. Mirrors build_b1_signal's contract exactly.
"""

from typing import Any

from trade.models import Candle
from trade.numbers import to_float
from trade.strategy.indicators import atr
from shared.strategies import ichi as _ichi

# Standard Ichimoku periods (9/26/52, 26-bar displacement).
TENKAN, KIJUN, SENKOU_B, DISP = 9, 26, 52, 26
# Minimum 4h candles: 52-bar Senkou B window read 26 bars back, plus warmup headroom.
MIN_CANDLES = 90


def _ichimoku_values(candles: list[Candle]):
    """Tenkan/Kijun at the last and prior bar plus the two cloud spans currently under
    price (built from the bar DISP back, so decision-time aligned). Returns
    (ten, ten_prev, kij, kij_prev, span_a, span_b) or None if history is short."""
    n = len(candles)
    if n < MIN_CANDLES:
        return None
    highs = [c.h for c in candles]
    lows = [c.l for c in candles]

    def mid(end: int, win: int) -> float:
        s = end - win + 1
        return (max(highs[s:end + 1]) + min(lows[s:end + 1])) / 2.0

    last = n - 1
    src = last - DISP
    if src - (SENKOU_B - 1) < 0:
        return None
    ten = mid(last, TENKAN)
    ten_prev = mid(last - 1, TENKAN)
    kij = mid(last, KIJUN)
    kij_prev = mid(last - 1, KIJUN)
    span_a = (mid(src, TENKAN) + mid(src, KIJUN)) / 2.0
    span_b = mid(src, SENKOU_B)
    return ten, ten_prev, kij, kij_prev, span_a, span_b


def build_ichimoku_tk_signal(coin: str, candles: list[Candle], candles_4h: list[Candle] | None,
                             ctx: dict[str, Any], allow_shorts: bool,
                             cfg: dict[str, Any] | None = None,
                             sr_cache: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """Ichimoku TK cross taken only in the cloud's direction, on the 4h timeframe.

    Reads candles_4h (the entry timeframe), not the 1h `candles`. Ignores sr_cache
    (no S/R dependency). Returns None until the 4h history is long enough.
    """
    cfg = cfg or {}
    c4 = candles_4h
    if not c4 or len(c4) < MIN_CANDLES:
        return None
    iv = _ichimoku_values(c4)
    if iv is None:
        return None
    ten, ten_prev, kij, kij_prev, span_a, span_b = iv

    a = atr(c4, int(to_float(cfg.get("atr_period"), 14)))     # 4h ATR (entry timeframe)
    if a is None:
        return None

    close = c4[-1].c
    cloud_top, cloud_bot = max(span_a, span_b), min(span_a, span_b)

    # Single source: shared.strategies.ichi. The point form gives only the last two bars of
    # Tenkan/Kijun + the spans under the current bar, so feed 2-element arrays and evaluate pos=1
    # (pos-1=0 is the prior bar). Proven identical to LAB's displaced-array form at the last bar.
    side = _ichi({"ich_ten": [ten_prev, ten], "ich_kij": [kij_prev, kij],
                  "ich_a": [span_a, span_a], "ich_b": [span_b, span_b],
                  "close": [close, close]}, 1)
    if side == "short" and not allow_shorts:
        side = None
    if side is None:
        return None

    funding = to_float(ctx.get("funding"), 0.0)
    edge = cloud_top if side == "long" else cloud_bot
    score = round(abs(ten - kij) / close * 100.0 + abs(close - edge) / close * 100.0, 4)

    return {
        "coin": coin, "side": side, "reason": "ichimoku_tk_cross",
        "score": score, "close": close, "atr": a, "size_mult": 1.0,
        "funding": funding,
        "sr_blocking_price": 0.0, "sr_blocking_touches": 0,
        # --- exit params (backtest TREND archetype) ---
        "strategy": "ICHI",
        "sl_mult": to_float(cfg.get("ichi_atr_sl_mult"), 2.0),
        "tp_mult": to_float(cfg.get("ichi_atr_tp_mult"), 4.0),
        "min_rr": to_float(cfg.get("ichi_min_rr"), 0.0),
        "use_sr_cap": False,
        "max_holding_hours": to_float(cfg.get("ichi_max_holding_hours"), 48),
    }
