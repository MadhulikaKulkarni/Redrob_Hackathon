def generate_reasoning(c, features):

    p = c["profile"]
    s = c["redrob_signals"]

    title = p["current_title"]
    exp = p["years_of_experience"]

    reasons = []

    if features["retrieval"] > 0:
        reasons.append(
            "retrieval and ranking systems"
        )

    if features["vector"] > 0:
        reasons.append(
            "vector search infrastructure"
        )

    if features["llm"] > 0:
        reasons.append(
            "LLM expertise"
        )

    if features["production"] > 0:
        reasons.append(
            "production ML systems"
        )

    if features["product"] > 0:
        reasons.append(
            "product engineering experience"
        )

    if len(reasons) == 0:
        reasons.append(
            "relevant AI experience"
        )

    reason = (
        f"{title} with "
        f"{exp:.1f} years of experience and "
        f"strength in {', '.join(reasons)}."
    )

    signals = []

    if s["open_to_work_flag"]:
        signals.append("open to work")

    if s["recruiter_response_rate"] > 0.7:
        signals.append("high recruiter responsiveness")

    if s["github_activity_score"] > 70:
        signals.append("strong GitHub activity")

    if s["saved_by_recruiters_30d"] > 10:
        signals.append("high recruiter interest")

    if len(signals) > 0:
        reason += (
            " Behavioral signals include "
            + ", ".join(signals)
            + "."
        )

    return reason