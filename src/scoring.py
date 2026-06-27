# =========================
# Title priors
# =========================

from honeypot import honeypot_penalty
GOOD_TITLES = [
    "ai engineer",
    "machine learning engineer",
    "ml engineer",
    "senior ai engineer",
    "senior machine learning engineer",
    "applied scientist",
    "data scientist",
    "nlp engineer",
    "search engineer",
    "recommendation engineer",
    "recommendation systems engineer",
    "retrieval engineer",
    "ranking engineer",
    "ai specialist",
    "ai research engineer",
]

BAD_TITLES = [
    "hr",
    "marketing",
    "content writer",
    "accountant",
    "sales",
    "graphic designer",
    "customer support",
]

NEUTRAL_TITLES = [
    "software engineer",
    "backend engineer",
    "data engineer",
    "analytics engineer",
    "project manager",
    "business analyst",
]


# =========================
# Career evidence
# =========================

GOOD_CAREER_WORDS = [
    "retrieval",
    "ranking",
    "recommendation",
    "recommender",
    "recommendation system",
    "search",
    "semantic search",
    "information retrieval",
    "matching",
    "candidate matching",
    "embeddings",
    "vector database",
    "faiss",
    "pinecone",
    "weaviate",
    "milvus",
    "qdrant",
    "elasticsearch",
    "opensearch",
    "llm",
    "transformer",
    "machine learning",
    "deep learning",
    "production",
    "deployed",
    "serving",
    "real users",
]

BAD_CAREER_WORDS = [
    "marketing campaign",
    "sales target",
    "customer service",
    "graphic design",
    "civil engineering",
    "mechanical design",
    "accounting",
    "bookkeeping",
    "payroll",
]


# =========================
# Title score
# =========================

def title_score(title):

    title = title.lower()

    for t in GOOD_TITLES:
        if t in title:
            return 2.0

    for t in BAD_TITLES:
        if t in title:
            return -2.0

    for t in NEUTRAL_TITLES:
        if t in title:
            return 0.5

    return 0.0


# =========================
# Experience score
# =========================

def experience_score(exp):

    if 5 <= exp <= 9:
        return 1.0

    if 4 <= exp <= 10:
        return 0.8

    if 3 <= exp <= 12:
        return 0.5

    return 0.2


# =========================
# Behavior score
# =========================

def behavior_score(c):

    s = c["redrob_signals"]

    score = 0

    if s["open_to_work_flag"]:
        score += 1

    score += s["recruiter_response_rate"]

    score += s["interview_completion_rate"]

    if s["github_activity_score"] > 0:
        score += s["github_activity_score"] / 100

    score += s["saved_by_recruiters_30d"] / 20

    if s["notice_period_days"] > 90:
        score -= 0.5

    elif s["notice_period_days"] > 30:
        score -= 0.2

    return score


# =========================
# Career score
# =========================

def career_score(c):

    text = ""

    for h in c["career_history"]:
        text += h["title"] + " "
        text += h["description"] + " "

    text = text.lower()

    score = 0

    for w in GOOD_CAREER_WORDS:
        if w in text:
            score += 1

    for w in BAD_CAREER_WORDS:
        if w in text:
            score -= 2

    score = max(min(score, 10), -5)

    return score

def honeypot_penalty(c):

    p = c["profile"]
    s = c["redrob_signals"]

    title = p["current_title"].lower()
    exp = p["years_of_experience"]

    penalty = 0

    # Impossible seniority
    if "senior" in title and exp < 3:
        penalty += 3

    if "staff" in title and exp < 5:
        penalty += 3

    if "lead" in title and exp < 5:
        penalty += 3

    # Unrealistic GitHub activity
    if (
        exp < 1
        and s["github_activity_score"] > 95
    ):
        penalty += 2

    # Recruiters save profile but candidate never replies
    if (
        s["saved_by_recruiters_30d"] > 30
        and s["recruiter_response_rate"] < 0.05
    ):
        penalty += 2

    # Completely inactive candidate
    if (
        not s["open_to_work_flag"]
        and s["recruiter_response_rate"] < 0.05
    ):
        penalty += 2

    return penalty


# =========================
# Final score
# =========================

def final_score(similarity, features, c):

    title = title_score(
        c["profile"]["current_title"]
    )

    exp = experience_score(
        c["profile"]["years_of_experience"]
    )

    behavior = behavior_score(c)

    career = career_score(c)

    feature_sum = (
          features["retrieval"]
        + features["vector"]
        + features["eval"]
        + features["llm"]
        + features["production"]
        + features["product"]
    )

    score = (
          similarity * 0.20
        + title * 0.25
        + career * 0.20
        + exp * 0.10
        + behavior * 0.10
        + feature_sum * 0.15
    )
    score -= honeypot_penalty(c)

    return float(score)