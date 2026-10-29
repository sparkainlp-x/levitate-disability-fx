"""Bank-API implications by country — study only, not legal advice.

Rules carried from the source study and the Zenodo framework:
- A bank API does NOT create grant eligibility, and a grant does NOT
  create bank-API access. Those are separate doors.
- Payment initiation is allowed in the model ONLY where a country
  profile verifies it AND a regulated partner is named. Otherwise
  the route is read-only verification or manual transfer, or UNKNOWN.
- No bank, platform, sponsor, or partner is named as agreeing to
  anything. Profiles are sourced-or-gap: anything not verified is
  "to collect", never invented.
- Disability detail is never sent to a bank API in this module:
  only aggregated, consented, minimum-necessary payment/identity
  fields, and only with a recorded consent gate.
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CountryProfile:
    country: str
    node: str
    regulator_or_framework: str
    read_only_available: str  # "yes" | "no" | "to collect"
    payment_initiation_available: str  # "yes" | "no" | "to collect"
    grant_disbursement_route: str
    consent_model: str
    key_risks: tuple
    to_collect: tuple = field(default_factory=tuple)
    source_note: str = ""


COUNTRY_PROFILES = {
    "CA-NB": CountryProfile(
        country="Canada",
        node="New Brunswick",
        regulator_or_framework=(
            "Consumer-Driven Banking Act (Royal Assent 26 Mar 2026, "
            "per framework); draft regulations pre-published 27 Jun 2026; "
            "phase 1 read-only; write/payment initiation is a later phase; "
            "Bank of Canada supervises. PIPEDA applies."),
        read_only_available="yes (phase 1, regulated participants only)",
        payment_initiation_available="no (later phase; to verify at use time)",
        grant_disbursement_route=(
            "Manual bank transfer via a regulated partner, or read-only "
            "account verification only. No API payment initiation in this study."),
        consent_model="Explicit, revocable, scope-limited consent; data minimisation; no disability detail shared.",
        key_risks=(
            "Assuming phase-1 read-only access equals payment access.",
            "Treating a grant award as bank-API onboarding.",
            "Sharing more than the minimum payment fields.",
        ),
        to_collect=("Local NB grant program rules", "Regulated partner identity", "Phase status at disbursement date"),
        source_note="Framework §§b.3/g, to verify locally; not legal advice.",
    ),
    "MA": CountryProfile(
        country="Morocco",
        node="Morocco (national)",
        regulator_or_framework=(
            "Law 09-08 (2009) on personal data; regulator CNDP. "
            "No open-banking framework identified in the framework; "
            "crypto-asset law 42-25 reported in consultation, not enacted "
            "as of mid-2026."),
        read_only_available="to collect",
        payment_initiation_available="no (default: no payment component)",
        grant_disbursement_route=(
            "Manual transfer via a local regulated partner only, after "
            "local legal check. Default: no API payment, no NFT component."),
        consent_model="Explicit consent under Law 09-08; CNDP guidance to collect; no disability detail shared.",
        key_risks=(
            "Assuming a Canadian open-banking pattern ports to Morocco.",
            "Any crypto/NFT payment route (default OFF, Bank Al-Maghrib warnings).",
        ),
        to_collect=("Open-banking status", "CNDP guidance on children's data", "Local grant disbursement rules"),
        source_note="Framework §b.4, secondary sources flagged there; verify locally.",
    ),
    "GENERIC": CountryProfile(
        country="Other",
        node="Template — fill before any use",
        regulator_or_framework="to collect",
        read_only_available="to collect",
        payment_initiation_available="to collect",
        grant_disbursement_route="UNKNOWN — do not disburse via API until verified.",
        consent_model="Explicit, revocable, scope-limited consent; no disability detail shared.",
        key_risks=("Inventing a bank-API route for an unverified country.",),
        to_collect=("Regulator", "Read/write status", "Grant rules", "Regulated partner"),
        source_note="Template only; every field must be sourced before use.",
    ),
}


def country_profile(code):
    """Return a CountryProfile, or the GENERIC template for unknown codes."""
    return COUNTRY_PROFILES.get(code, COUNTRY_PROFILES["GENERIC"])


def bank_api_implication(code, regulated_partner_named=False, consent_recorded=False):
    """Return the bank-API implication for a grant in this country.

    Fail-closed: payment initiation is 'allowed' only if the profile
    says yes AND a regulated partner is named AND consent is recorded.
    Otherwise the answer is the safe route, with the reason stated.
    """
    p = country_profile(code)
    if (p.payment_initiation_available.startswith("yes")
            and regulated_partner_named and consent_recorded):
        route = "API payment initiation (verified profile + regulated partner + consent)"
        allowed = True
    else:
        route = p.grant_disbursement_route
        allowed = False
    reasons = []
    if not p.payment_initiation_available.startswith("yes"):
        reasons.append("payment initiation not verified for this country")
    if not regulated_partner_named:
        reasons.append("no regulated partner named")
    if not consent_recorded:
        reasons.append("no consent recorded")
    return {
        "tag": "STUDY",
        "country": p.country,
        "node": p.node,
        "read_only_available": p.read_only_available,
        "payment_initiation_available": p.payment_initiation_available,
        "api_payment_allowed": allowed,
        "grant_disbursement_route": route,
        "blocked_reasons": reasons,
        "key_risks": list(p.key_risks),
        "to_collect": list(p.to_collect),
        "note": "A bank API does not create grant eligibility. A grant does not create bank-API access.",
    }
