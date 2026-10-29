"""Synthetic demo. Run: python3 demo.py (from the package root, with src on path)."""
import sys
sys.path.insert(0, "src")
from levitate_disability_fx import (
    Adoption, adoption_lift, country_profile, bank_api_implication,
    GrantFlow, grant_implications, NINETY_DAY_PLAN, go_no_go,
)

cohort = Adoption(enrolled=200, onboarded=150, returned=120,
                  organiser_minutes_saved_per_session=15, sessions=12,
                  review_board_signoff=True)
adopt = adoption_lift(cohort, baseline_return_rate=0.40, baseline_onboarding_rate=0.60)
print("ADOPTION (SYNTHETIC):", adopt)

for code in ("CA-NB", "MA", "GENERIC"):
    print(code, bank_api_implication(code, regulated_partner_named=True, consent_recorded=True))

bank = bank_api_implication("CA-NB", regulated_partner_named=True, consent_recorded=True)
grant = grant_implications(
    GrantFlow(country_code="CA-NB", grant_amount_cu=50000, sponsor_share=0.4,
              review_board_signoff=True, regulated_partner_named=True, consent_recorded=True),
    bank)
print("GRANT (STUDY):", grant)
print("GO/NO-GO:", go_no_go(adopt, grant, platform_gate_passed=True))
print("PLAN RULE:", NINETY_DAY_PLAN["rule_pick_one_door"])
