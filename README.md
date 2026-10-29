# Levitate disability-led FX — upgrade module v0.1.0

**STUDY ONLY. Not a partnership, not a grant application, not a bank integration, not a medical device, not a forecast.**

An upgrade add-on to the country-prototype-kit idea: it lifts ("levitates")
disability-led participation effects into a measurable, gated form, and it
maps what a bank API can and cannot do for a grant, country by country.

It does **not** replace the country-prototype-kit, does **not** change its
synthetic Economic Flip numbers, does **not** merge Zoom and Microsoft into
one bid, and does **not** merge with any ACOA, NBIF, or Breakthru work.

## What is in it

| Module | What it does |
|---|---|
| `adoption.py` | Participation lift (onboarding, return rate, organiser time saved) with a Wilson-interval claim gate. No claim without a large-enough sample, a lower bound clearing baseline + smallest effect, and review-board signoff. |
| `bank_api.py` | Country profiles, sourced-or-gap: Canada–NB, Morocco, and a blank template. Payment initiation is fail-closed: allowed only if verified for that country AND a regulated partner is named AND consent is recorded. |
| `grant.py` | Grant flow with a sponsor firewall: sponsors fund, they never decide eligibility. Carries the source study's do-not-claim list. |
| `plan.py` | The 90-day plan in the source study's shape: pick ONE door first (Zoom OR Microsoft), cash lane = physical display sold separately, go/no-go at day 90. |

## The do-not-claim list (from the source study)

- No signed Zoom or Microsoft partnership. No Marketplace/Store listing until review.
- No medical, diagnostic, or HoloHeal-as-therapy claim. HoloHeal stays research / wellness-adjacent.
- No quantum-computer claim inside a meeting app.
- No $3.85M ARR, 150k users, or guaranteed Azure uplift until invoices exist.
- No Avalon / NOVAC resale inside Zoom or Teams.
- No bank, sponsor, or platform is named as agreeing to anything in this study.
- No grant eligibility is created by a bank API, and no bank-API access is created by a grant.

## Bank-API implications, in one paragraph per country

**Canada–NB:** open banking is phase-1 read-only for regulated participants;
write/payment initiation is a later phase. So in this study the route is
manual transfer via a regulated partner, or read-only verification only.
**Morocco:** no open-banking framework identified; Law 09-08 / CNDP apply;
default is no API payment and no NFT component. **Any other country:** the
template says UNKNOWN on every field until sourced — do not disburse via API.

## Demo (synthetic)

```bash
python3 demo.py
python3 -m unittest discover -s tests -v
```

Demo cohort (synthetic, 200 enrolled, 150 onboarded, 120 returned,
baseline return 0.40, signoff recorded): return rate 0.60, Wilson 95%
0.531–0.665, lift +0.20 — claim allowed only because the lower bound
0.531 clears baseline + 0.10 (= 0.50) and signoff is recorded.
With baseline 0.45 the same cohort would NOT clear the gate (0.531 < 0.55) —
that is the gate working, and the demo uses 0.40 so the passing case is honest. Change any of those and
the gate withholds the claim. That is the point.

## Licence

AGPL-3.0-only for this module's code. The source study PDF and the Zenodo
framework text it builds on keep their own licences; nothing here re-licences them.
