# src/honeypot.py

def honeypot_penalty(c):

    penalty = 0

    p = c["profile"]
    s = c["redrob_signals"]

    title = (
        p["current_title"]
        .lower()
        .strip()
    )

    exp = p["years_of_experience"]

    # ==========================
    # Impossible seniority
    # ==========================

    if "senior" in title and exp < 3:
        penalty += 3

    if "staff" in title and exp < 5:
        penalty += 3

    if "lead" in title and exp < 5:
        penalty += 3

    if "principal" in title and exp < 7:
        penalty += 3

    # ==========================
    # Unrealistic GitHub score
    # ==========================

    if (
        exp < 1
        and s["github_activity_score"] > 95
    ):
        penalty += 2

    # ==========================
    # Recruiters love profile
    # but candidate never replies
    # ==========================

    if (
        s["saved_by_recruiters_30d"] > 30
        and s["recruiter_response_rate"] < 0.05
    ):
        penalty += 2

    # ==========================
    # Completely inactive profile
    # ==========================

    if (
        not s["open_to_work_flag"]
        and s["recruiter_response_rate"] < 0.05
    ):
        penalty += 2

    # ==========================
    # Never attends interviews
    # ==========================

    if (
        s["interview_completion_rate"] < 0.10
        and s["saved_by_recruiters_30d"] > 20
    ):
        penalty += 2

    # ==========================
    # Huge notice period
    # ==========================

    if s["notice_period_days"] > 120:
        penalty += 1

    # ==========================
    # Unverified profile
    # ==========================

    if (
        not s["verified_email"]
        and not s["verified_phone"]
    ):
        penalty += 1

    return penalty