#!/usr/bin/env python3
"""
Cost model for the FOREX backtest gauntlet. (updated 2026-06-06)

SINGLE-VENUE, anchored to OSTIUM -- mirroring how sister-lab's stress test anchors to Hyperliquid.
The BASE cost is the venue we actually trade (Ostium realistic-worst); the STRESS test DEGRADES
that same base (higher fee / slippage / holding). It does NOT stack the worst of several brokers
-- that "Frankenstein venue" exists nowhere and would reject edges that are genuinely profitable
on Ostium (false negatives = thrown-away opportunity). Frankenstein is explicitly NOT used
(the operator, 2026-06-06). sister-lab does the same thing: base = Hyperliquid 4.5 bps/side + 1 bp slip,
stress = fee +25/50% and slip -> 3/5 bps; one venue, degraded.

Cost rules (GAUNTLET.md): each cost on its OWN axis -- per-trade (fee + spread) scales with trade
COUNT; holding (rollover) scales with TIME; slippage scales with SIZE and VOLATILITY (fat-tail
floor). The engine calls each at the right axis; never summed into one flat number here.

All fees in basis points (1 bp = 0.01%). Spread is ROUND-TRIP.

OSTIUM GROUND TRUTH (verified 2026-06-06 from the live subgraph + SDK v3.2.1 + docs.ostium.com):
  - Opening fee = 0.03% (3 bps), FIXED regardless of leverage/OI skew. Closing fee = 0%.
  - Oracle fee = $0.10 FLAT per manual close (refunded on a successful full close, not on failure).
    A fixed-$ cost -> it dominates on tiny positions, so it gates minimum size (see oracle_fee_usd).
  - Spread is DYNAMIC ("Price-After-Impact"): 0% while short-term net volume is below a threshold,
    then a spread + OI-skew impact. So baseline ~0; the spread_bps_* below are worst-realistic
    impact estimates for entering against skew, NOT a constant cost.
  - Rollover (carry) = the holding cost, per-pair + dynamic (interest-rate diff + storage), updated
    daily on-chain. Real 24h samples: EUR/USD ~0.27 bp, XAU/USD ~1.55 bp, Brent ~0. holding_bps_
    per_day below is a conservative worst-realistic single value; Stage-2 may read per-pair live.
  - Funding (skew-based) is primarily a sister-lab mechanism; for our FX/commodity universe it is ~0,
    so it is NOT modelled separately (rollover already carries the cost).
  - Max leverage is per-pair (FX up to 200x, metals/energy ~100x); MAX_SL 85%, liq at -90% of
    collateral, profit capped at +900%.
RE-VERIFY before live (rollover/funding drift daily; fees can change).
"""

from dataclasses import dataclass, field

# Asset classes (pick the right spread). Plain strings, JSON-friendly, set per catalog entry.
MAJOR = "major"          # EUR/USD, USD/JPY, GBP/USD, USD/CHF, AUD/USD, USD/CAD, NZD/USD
CROSS = "cross"          # EUR/JPY
COMMODITY = "commodity"  # XAU, XAG, BCO(Brent), WTI, COPPER, NATGAS
EXOTIC = "exotic"        # USD/ZAR, USD/MXN


@dataclass(frozen=True)
class VenueProfile:
    """Worst-realistic coherent cost set for ONE venue. Only OSTIUM is used (single-venue).

    Costs are realistic-PER-ASSET-CLASS, not worst-uniform: a major's spread/rollover genuinely is
    lower than an exotic's, so charging every pair the worst pair's cost would over-penalise majors
    and reject edges that are genuinely profitable on Ostium (false negatives -- the anti-Frankenstein
    rule, GAUNTLET.md). The margin of safety lives in the STRESS layer (degraded multipliers), NOT in
    an inflated base. SLIPPAGE is volatility-scaled per bar (the real killer, rule 3) rather than a
    flat pip: floor + slip_vol_frac * (ATR-as-bps), capped at slip_cap_bps for the fat tail."""
    name: str
    open_fee_bps: float
    close_fee_bps: float
    spread_bps_major: float
    spread_bps_cross: float
    spread_bps_commodity: float
    spread_bps_exotic: float
    # Rollover/carry per asset class, bps/day (real: EUR ~0.27, XAU ~1.55, Brent ~0; exotics carry a
    # bigger interest-rate-diff). Per-class, not one worst-uniform number.
    holding_bps_major: float
    holding_bps_cross: float
    holding_bps_commodity: float
    holding_bps_exotic: float
    # Slippage = floor + slip_vol_frac*(ATR/price in bps), clamped to [floor, slip_cap_bps].
    slippage_floor_bps: float
    slip_vol_frac: float
    slip_cap_bps: float
    oracle_fee_usd: float = 0.0   # fixed $ cost per manual close (Ostium $0.10); engine -> bps via notional
    notes: str = ""

    def spread_bps(self, asset_class):
        return {MAJOR: self.spread_bps_major, CROSS: self.spread_bps_cross,
                COMMODITY: self.spread_bps_commodity, EXOTIC: self.spread_bps_exotic}[asset_class]

    def holding_per_day(self, asset_class):
        """Rollover/carry bps/day for an asset class (the holding cost axis)."""
        return {MAJOR: self.holding_bps_major, CROSS: self.holding_bps_cross,
                COMMODITY: self.holding_bps_commodity, EXOTIC: self.holding_bps_exotic}[asset_class]


# The ONE venue in the cost model. BASE cost = this profile at multiplier 1.0.
OSTIUM = VenueProfile(
    name="ostium",
    open_fee_bps=3.0,            # 0.03% fixed opening fee (verified live: takerFeeP 30000/1e6)
    close_fee_bps=0.0,          # no closing fee
    # Spread is DYNAMIC (~0 baseline); these are worst-realistic OI-skew IMPACT estimates, not constants.
    spread_bps_major=1.0,
    spread_bps_cross=2.0,
    spread_bps_commodity=3.0,
    spread_bps_exotic=4.0,
    # Rollover/carry per class (real 24h: EUR ~0.27, XAU ~1.55, Brent ~0; exotics higher rate-diff).
    # Conservative-realistic per class; funding ~0 for FX. Stress x2 in the harsh scenario.
    holding_bps_major=0.5,
    holding_bps_cross=1.0,
    holding_bps_commodity=2.0,
    holding_bps_exotic=3.0,
    # Slippage: floor 1.5 bps + 5% of the bar's ATR (in bps), capped 50 bps (fat tail). Replaces the
    # old flat 1.5: slippage is the real killer and scales with volatility (GAUNTLET.md rule 3). The
    # SIZE term is omitted -- price-impact is dust for the $1000 research bankroll on Ostium's books;
    # revisit (add a size term) only when sizing up. TUNING BAND: slip_vol_frac 0.03 (calmer) .. 0.10
    # (harsher); slip_cap_bps 30 (tighter) .. 80 (wider tail). Recalibrate vs measured Ostium fills.
    slippage_floor_bps=1.5,
    slip_vol_frac=0.05,
    slip_cap_bps=50.0,
    oracle_fee_usd=0.10,         # $0.10 flat per manual close (gates minimum position size)
    notes="the ONLY venue; BASE = real Ostium at mult 1.0, stress degrades it. Verified 2026-06-06.",
)

# Stress scenarios = DEGRADE the Ostium base (direct analog of sister-lab's HL fee+25/50% & slip x).
#   fee_mult  scales the per-trade FEE leg (open+close fee)
#   slip_mult scales the EXECUTION leg (spread + slippage)
#   hold_mult scales the HOLDING leg (rollover/day)
BASE = {"fee_mult": 1.0, "slip_mult": 1.0, "hold_mult": 1.0}
STRESS_SCENARIOS = {
    "base":     BASE,
    "fee_+25%": {"fee_mult": 1.25, "slip_mult": 1.0, "hold_mult": 1.0},
    "fee_+50%": {"fee_mult": 1.50, "slip_mult": 1.0, "hold_mult": 1.0},
    "slip_2x":  {"fee_mult": 1.0,  "slip_mult": 2.0, "hold_mult": 1.0},
    "slip_3x":  {"fee_mult": 1.0,  "slip_mult": 3.0, "hold_mult": 1.0},
    "harsh":    {"fee_mult": 1.5,  "slip_mult": 3.0, "hold_mult": 2.0},  # verdict scenario
}
VERDICT_SCENARIO = "harsh"
SURVIVE_PF = 1.0  # a strategy survives stress if pooled PF >= this at the verdict scenario


def slippage_bps(profile, atr_pct):
    """Volatility-scaled slippage in bps for ONE bar (rule 3): floor + slip_vol_frac*(ATR-as-bps),
    clamped to [floor, slip_cap_bps]. atr_pct = ATR/price (the engine's I['atr_pct']); NaN -> floor.
    Single source of the slippage formula -- slip_fraction_array vectorises THIS for the engine."""
    if atr_pct != atr_pct:                       # NaN warm-up bar -> floor only
        return profile.slippage_floor_bps
    bps = profile.slippage_floor_bps + profile.slip_vol_frac * (atr_pct * 10_000.0)
    return min(max(bps, profile.slippage_floor_bps), profile.slip_cap_bps)


def slip_fraction_array(profile, atr_pct, slip_mult):
    """Per-bar slippage as a FRACTION (bps/1e4), vectorised over an atr_pct numpy array, then scaled
    by the scenario slip_mult. Same formula as slippage_bps -- engine calls this once per run so the
    per-bar volatility-scaled slippage costs nothing in the bar loop."""
    import numpy as np
    vol_bps = np.where(np.isfinite(atr_pct), atr_pct * 10_000.0, 0.0)
    bps = np.clip(profile.slippage_floor_bps + profile.slip_vol_frac * vol_bps,
                  profile.slippage_floor_bps, profile.slip_cap_bps)
    return (bps / 10_000.0) * slip_mult


@dataclass(frozen=True)
class CostModel:
    """Ostium profile + a stress scenario (multipliers). BASE scenario = the GATE cost. The
    engine calls per_trade_bps / holding_bps / slippage at the right axis (rule 2)."""
    profile: VenueProfile = OSTIUM
    scenario: dict = field(default_factory=lambda: dict(BASE))

    def per_trade_bps(self, asset_class):
        """Round-trip per-trade cost (fee leg + spread leg) for one trade, in bps."""
        p, s = self.profile, self.scenario
        fee = (p.open_fee_bps + p.close_fee_bps) * s["fee_mult"]
        spread = p.spread_bps(asset_class) * s["slip_mult"]
        return fee + spread

    def holding_bps(self, days_held, asset_class):
        return self.profile.holding_per_day(asset_class) * days_held * self.scenario["hold_mult"]

    def slippage(self, atr_pct):
        """Volatility-scaled slippage FRACTION for one bar (bps/1e4), scenario-scaled."""
        return (slippage_bps(self.profile, atr_pct) / 10_000.0) * self.scenario["slip_mult"]


def for_scenario(name):
    """CostModel for a named stress scenario on the Ostium base."""
    return CostModel(OSTIUM, STRESS_SCENARIOS[name])


# The hard eligibility cost: Ostium realistic, no degradation. The GATE runs on this.
GATE = for_scenario("base")
