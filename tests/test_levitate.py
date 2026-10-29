import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import unittest
from levitate_disability_fx import (
    Adoption, adoption_lift, wilson_interval, country_profile,
    bank_api_implication, GrantFlow, grant_implications,
    NINETY_DAY_PLAN, go_no_go,
)

class TestAdoption(unittest.TestCase):
    def test_wilson_empty(self):
        self.assertEqual(wilson_interval(0, 0), (0.0, 0.0))
    def test_wilson_bounds(self):
        low, high = wilson_interval(120, 200)
        self.assertTrue(0 < low < 0.6 < high < 1)
    def test_claim_allowed_with_signoff_and_clear_bound(self):
        c = Adoption(200, 150, 120, review_board_signoff=True)
        r = adoption_lift(c, 0.40, 0.60)
        self.assertTrue(r["claim_allowed"])
        self.assertEqual(r["tag"], "SYNTHETIC")
        self.assertAlmostEqual(r["return_rate"], 0.6)
    def test_claim_withheld_without_signoff(self):
        c = Adoption(200, 150, 120, review_board_signoff=False)
        r = adoption_lift(c, 0.45)
        self.assertFalse(r["claim_allowed"])
        self.assertIsNone(r["claim"])
    def test_claim_withheld_small_sample(self):
        c = Adoption(10, 8, 7, review_board_signoff=True)
        r = adoption_lift(c, 0.45)
        # Wilson low for 7/10 is ~0.40, below 0.45+0.10=0.55
        self.assertFalse(r["claim_allowed"])
    def test_invalid_counts(self):
        with self.assertRaises(ValueError):
            Adoption(10, 11, 5)

class TestBankApi(unittest.TestCase):
    def test_canada_no_payment_initiation(self):
        r = bank_api_implication("CA-NB", True, True)
        self.assertFalse(r["api_payment_allowed"])
        self.assertIn("payment initiation not verified", "; ".join(r["blocked_reasons"]))
    def test_morocco_default_no_payment(self):
        r = bank_api_implication("MA", True, True)
        self.assertFalse(r["api_payment_allowed"])
        self.assertEqual(r["payment_initiation_available"][:2], "no")
    def test_generic_unknown(self):
        r = bank_api_implication("XX", True, True)
        self.assertFalse(r["api_payment_allowed"])
        self.assertIn("UNKNOWN", r["grant_disbursement_route"])
    def test_profile_fields(self):
        p = country_profile("CA-NB")
        self.assertEqual(p.country, "Canada")
        self.assertTrue(p.to_collect)

class TestGrantPlan(unittest.TestCase):
    def test_grant_blocks_api_when_bank_blocks(self):
        bank = bank_api_implication("CA-NB", True, True)
        g = grant_implications(GrantFlow("CA-NB", 50000, 0.4, True, True, True), bank)
        self.assertFalse(g["api_disbursement_allowed"])
        self.assertTrue(g["reporting_allowed"])
        self.assertTrue(g["sponsor_firewall_proven"])
        self.assertIn("No signed Zoom", g["do_not_claim"][0])
    def test_grant_no_reporting_without_signoff(self):
        bank = bank_api_implication("CA-NB", True, True)
        g = grant_implications(GrantFlow("CA-NB", 50000, 0.4, False, True, True), bank)
        self.assertFalse(g["reporting_allowed"])
        self.assertFalse(g["sponsor_firewall_proven"])
    def test_sponsor_share_validation(self):
        with self.assertRaises(ValueError):
            GrantFlow("CA-NB", 100, 1.5)
    def test_go_no_go(self):
        adopt = {"claim_allowed": True, "withheld_reason": None}
        grant = {"reporting_allowed": True}
        self.assertEqual(go_no_go(adopt, grant, True)["decision"], "GO")
        self.assertEqual(go_no_go(adopt, grant, False)["decision"], "STOP_OR_REDESIGN")
    def test_plan_pick_one_door(self):
        self.assertIn("not both", NINETY_DAY_PLAN["rule_pick_one_door"])
        self.assertEqual(len(NINETY_DAY_PLAN["days_1_30"]), 4)

if __name__ == "__main__":
    unittest.main()
