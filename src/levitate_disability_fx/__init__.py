"""Levitate disability-led FX — study-only upgrade module.

STUDY ONLY. Not a partnership, not a grant application, not a bank
integration, not a medical device, not a forecast. All numbers in the
demo are SYNTHETIC illustrations. See README.md and PLAN.md.
"""
__version__ = "0.1.0"
from .adoption import Adoption, adoption_lift, wilson_interval
from .bank_api import COUNTRY_PROFILES, country_profile, bank_api_implication
from .grant import GrantFlow, grant_implications
from .plan import NINETY_DAY_PLAN, go_no_go

__all__ = [
    "__version__", "Adoption", "adoption_lift", "wilson_interval",
    "COUNTRY_PROFILES", "country_profile", "bank_api_implication",
    "GrantFlow", "grant_implications", "NINETY_DAY_PLAN", "go_no_go",
]
