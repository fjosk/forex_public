"""
Single source of truth for the EXIT-level math shared by LAB (backtest engine) and TRADE
(paper + exchange execution). These are the generic ATR-exit primitives every strategy rides on
(the per-strategy exit *config* -- sl/tp mults, time stop, chandelier mult -- is carried on the
signal; this module is the arithmetic that turns that config into stop/target/trail levels).

Each function preserves the EXACT operand order of the three call sites it replaces, so the result
is bit-identical to the prior inline expressions (verified: LAB backtest 0-diff + a paper
exit-scenario byte-equality harness). `direction` is +1 for long / -1 for short (int or float;
both exact). Orchestration -- when to size, when to check, how to place orders -- stays in each
caller; only the formulas live here.

NOTE: this couples the live trader to the shared package. That is the deliberate Phase C decision
(the LAB<->TRADE firewall was overridden); keep these functions pure and never add I/O or state.
"""


def stop_distance(atr, sl_mult, ref_px, min_stop_pct):
    """ATR stop distance, floored at a min percentage of the reference price.
    ref_px is entry for paper/backtest, mark/fill for the exchange path (documented divergence).

    CONTRACT: the return can be <= 0 when ref_px <= 0 (or both atr and the floor are <= 0).
    Callers divide qty = risk / stop_distance, so EVERY caller MUST guard `stop_distance <= 0`
    and skip the trade. The guard lives in the callers (paper calc_open_order, exchange
    execute_open, LAB engine _size) -- not here -- to keep this primitive bit-identical to the
    original inline expressions (0-diff harness). Do not add a floor here without re-running it.

    NaN ATR (corrected 2026-06-03): `max(atr*sl_mult, floor)` has the ATR term FIRST, and
    `max(nan, x)` returns NaN (all NaN comparisons are False, so the first operand wins). So a
    NaN atr makes this return NaN -- it does NOT coerce to the floor -- and `nan <= 0` is False,
    so the `stop_distance <= 0` caller guard does NOT catch it (NaN would flow into qty = risk /
    NaN = NaN). Callers MUST therefore reject a non-finite or <= 0 atr explicitly BEFORE calling
    (paper/exchange do this via to_float, which maps NaN/inf -> 0.0, then guard atr_v <= 0)."""
    return max(atr * sl_mult, ref_px * min_stop_pct)


def initial_stop(ref_px, direction, dist):
    """Initial protective stop: ref_px - direction * dist."""
    return ref_px - direction * dist


def initial_target(ref_px, direction, atr, tp_mult):
    """ATR take-profit level: ref_px + direction * atr * tp_mult. Caller guards tp_mult > 0."""
    return ref_px + direction * atr * tp_mult


def profit_r(direction, best, entry, dist):
    """Open profit in R multiples (favourable excursion / initial stop distance)."""
    return direction * (best - entry) / dist


def chandelier_stop(best, direction, chand_mult, atr):
    """Chandelier trailing stop: best - direction * chand_mult * atr."""
    return best - direction * chand_mult * atr


def breakeven_stop(entry, direction, dist):
    """Break-even-plus stop (entry + 0.1R) used as a floor once the trail activates."""
    return entry + direction * dist * 0.1


def tighten_stop(current, chand, be, direction):
    """Ratchet the stop in the trade's favour only: max for long, min for short."""
    return max(current, chand, be) if direction > 0 else min(current, chand, be)
