"""Disability-led adoption: participation lift, fail-closed.

Levitate FX = the *effect* of a participation layer, measured as lift
in onboarding completion, return rate, and organiser time saved.
It is NOT a medical, diagnostic, or therapy effect, and it is NOT
a claim about any real person: intake is optional, data is minimum,
organiser analytics stay aggregated, no disability detail is disclosed.

A claim is emitted only if: the sample is large enough for the
pre-registered smallest effect, the Wilson lower bound clears it,
and a human review-board signoff is recorded. Otherwise: no claim.
"""
import math
from dataclasses import dataclass


def wilson_interval(k, n, z=1.96):
    """Wilson 95% interval for k/n. Returns (low, high) or (0, 0) if n==0."""
    if n <= 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


@dataclass
class Adoption:
    """One synthetic adoption cohort. All inputs are study assumptions."""
    enrolled: int
    onboarded: int
    returned: int
    organiser_minutes_saved_per_session: float = 0.0
    sessions: int = 0
    review_board_signoff: bool = False
    smallest_effect_of_interest: float = 0.10

    def __post_init__(self):
        if not (0 <= self.onboarded <= self.enrolled):
            raise ValueError("onboarded must be between 0 and enrolled")
        if not (0 <= self.returned <= self.enrolled):
            raise ValueError("returned must be between 0 and enrolled")
        if self.enrolled < 0 or self.sessions < 0:
            raise ValueError("counts must be non-negative")

    @property
    def onboarding_rate(self):
        return self.onboarded / self.enrolled if self.enrolled else 0.0

    @property
    def return_rate(self):
        return self.returned / self.enrolled if self.enrolled else 0.0


def adoption_lift(cohort, baseline_return_rate, baseline_onboarding_rate=0.0):
    """Return a dict tagged SYNTHETIC, with a claim gate.

    Lift = cohort rate - baseline rate. No claim is emitted unless
    the Wilson lower bound on the return rate clears
    baseline + smallest_effect AND review signoff is recorded.
    With a small sample, the interval is wide and the gate fails —
    that is the gate working, not a bug.
    """
    low, high = wilson_interval(cohort.returned, cohort.enrolled)
    lift = cohort.return_rate - baseline_return_rate
    gate_pass = (
        cohort.review_board_signoff
        and low > baseline_return_rate + cohort.smallest_effect_of_interest
    )
    return {
        "tag": "SYNTHETIC",
        "enrolled": cohort.enrolled,
        "onboarding_rate": round(cohort.onboarding_rate, 4),
        "return_rate": round(cohort.return_rate, 4),
        "return_rate_wilson_95": (round(low, 4), round(high, 4)),
        "return_lift_vs_baseline": round(lift, 4),
        "onboarding_lift_vs_baseline": round(
            cohort.onboarding_rate - baseline_onboarding_rate, 4),
        "organiser_minutes_saved_total": round(
            cohort.organiser_minutes_saved_per_session * cohort.sessions, 1),
        "claim_allowed": gate_pass,
        "claim": (
            f"Return rate {cohort.return_rate:.3f} (Wilson 95% {low:.3f}-{high:.3f}) "
            f"clears baseline + smallest effect."
            if gate_pass else None),
        "withheld_reason": None if gate_pass else (
            "no review-board signoff" if not cohort.review_board_signoff
            else "Wilson lower bound does not clear baseline + smallest effect"),
    }
