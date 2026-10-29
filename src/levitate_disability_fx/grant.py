"""Grant implications for disability-led adoption solutions.

A grant is a funding decision with its own rules, evidence, and
audit trail. It is NOT a platform partnership, NOT a bank integration,
and NOT a purchase. This module keeps three lanes separate:
  1. Grant lane: eligibility, evidence, disbursement, reporting.
  2. Platform lane: Zoom OR Microsoft — pick ONE door first, never
     both in the same bid, budget, or success metric (source study).
  3. Bank lane: payment rails only, via a regulated partner, with
     a sponsor firewall (sponsors never decide eligibility).

Do-not-claim list, carried verbatim in spirit from the source study:
no signed Zoom/Microsoft partnership, no Marketplace listing until
review, no medical/diagnostic claim, no HoloHeal-as-therapy claim,
no quantum-computer claim inside a meeting app, no $3.85M ARR /
150k users / guaranteed Azure uplift figure until invoices exist.
"""
from dataclasses import dataclass


DO_NOT_CLAIM = (
    "No signed Zoom or Microsoft partnership.",
    "No Marketplace/Store listing until review.",
    "No medical, diagnostic, or HoloHeal-as-therapy claim.",
    "No quantum-computer claim inside a meeting app.",
    "No $3.85M ARR, 150k users, or guaranteed Azure uplift until invoices exist.",
    "No Avalon/NOVAC resale inside Zoom or Teams.",
)


@dataclass
class GrantFlow:
    """One synthetic grant flow. All values are study assumptions."""
    country_code: str
    grant_amount_cu: float
    sponsor_share: float  # 0..1 of cost covered by a sponsor
    review_board_signoff: bool = False
    regulated_partner_named: bool = False
    consent_recorded: bool = False

    def __post_init__(self):
        if not (0 <= self.sponsor_share <= 1):
            raise ValueError("sponsor_share must be between 0 and 1")
        if self.grant_amount_cu < 0:
            raise ValueError("grant_amount_cu must be non-negative")


def grant_implications(flow, bank_implication):
    """Combine a grant flow with a bank-API implication, fail-closed.

    Disbursement via API is allowed only if the bank implication
    allows it. Reporting is allowed only with review signoff.
    Sponsor share is reported, never allowed to decide eligibility:
    the firewall flag is True only if sponsor_share < 1 and the
    eligibility decision is recorded as independent — in this study
    model that independence must be asserted by the caller via
    review_board_signoff, otherwise the firewall is reported as
    unproven, not as passed.
    """
    api_ok = bank_implication["api_payment_allowed"]
    return {
        "tag": "STUDY",
        "country_code": flow.country_code,
        "grant_amount_cu": flow.grant_amount_cu,
        "sponsor_share": flow.sponsor_share,
        "disbursement_route": (
            bank_implication["grant_disbursement_route"] if api_ok
            else "Manual transfer via regulated partner (API route blocked: "
            + "; ".join(bank_implication["blocked_reasons"]) + ")"),
        "api_disbursement_allowed": api_ok,
        "reporting_allowed": flow.review_board_signoff,
        "sponsor_firewall_proven": flow.review_board_signoff and flow.sponsor_share < 1,
        "sponsor_firewall_note": (
            "Sponsors fund; they do not decide eligibility. "
            "Firewall is proven only with independent review signoff."),
        "do_not_claim": list(DO_NOT_CLAIM),
    }
