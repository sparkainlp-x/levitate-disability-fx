"""90-day plan, in the shape of the source study. STUDY ONLY.

Same shape on either platform, but pick ONE door first:
Zoom proof-of-value OR Microsoft for Startups — not both in the
same week, same bid, or same success metric. The cash lane while
platforms review is the physical Fredericton display, sold
separately; it does not wait on Zoom or Microsoft.
"""
NINETY_DAY_PLAN = {
    "tag": "STUDY",
    "rule_pick_one_door": "Zoom proof-of-value OR Microsoft for Startups — not both in the same week.",
    "cash_lane": "Physical Fredericton POV LED-fan display, sold separately; does not wait on platforms.",
    "days_1_30": [
        "Pick one platform. Confirm SDK / Store path.",
        "Write the data-minimisation note.",
        "Recruit 3 disability-led creators + 1-3 partner orgs.",
        "Record a real session on existing tools.",
    ],
    "days_31_60": [
        "Run recurring sessions (not one spike).",
        "Log onboarding completion, mode chosen, return rate, organiser time saved.",
        "Keep holography off unless the venue is already booked.",
    ],
    "days_61_90": [
        "Scorecard + privacy report + accessibility notes.",
        "Go / no-go: Marketplace/Store beta, or stop and keep selling physical displays.",
    ],
    "metrics": [
        "onboarding completion", "mode chosen", "return rate", "organiser time saved",
    ],
    "metrics_not_collected": [
        "diagnoses", "medical detail", "disability detail disclosed publicly",
    ],
}


def go_no_go(adoption_result, grant_result, platform_gate_passed):
    """Go only if adoption claim, grant reporting, and platform gate all pass.

    Otherwise the decision is STOP or REDESIGN, with the reasons
    listed — never a soft 'go' on a partial pass.
    """
    reasons = []
    if not adoption_result["claim_allowed"]:
        reasons.append("adoption claim not allowed: " + str(adoption_result["withheld_reason"]))
    if not grant_result["reporting_allowed"]:
        reasons.append("grant reporting not allowed: no review-board signoff")
    if not platform_gate_passed:
        reasons.append("platform gate not passed (SDK/Store path, privacy, accessibility, legal)")
    return {
        "tag": "STUDY",
        "decision": "GO" if not reasons else "STOP_OR_REDESIGN",
        "reasons": reasons,
    }
