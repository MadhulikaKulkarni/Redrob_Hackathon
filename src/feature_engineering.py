# ===============================
# Build candidate text
# ===============================

def build_candidate_text(c):

    text = ""

    p = c["profile"]

    text += p.get("headline", "") + " "
    text += p.get("summary", "") + " "
    text += p.get("current_title", "") + " "
    text += p.get("current_industry", "") + " "

    # Career History
    for h in c.get("career_history", []):
        text += h.get("title", "") + " "
        text += h.get("description", "") + " "
        text += h.get("industry", "") + " "

    # Skills
    for s in c.get("skills", []):
        text += s.get("name", "") + " "

    # Education
    for e in c.get("education", []):
        text += e.get("degree", "") + " "
        text += e.get("field_of_study", "") + " "

    return text.lower()


# ===============================
# Keywords
# ===============================

RETRIEVAL_WORDS = [
    "retrieval",
    "search",
    "ranking",
    "recommendation",
    "recommender",
    "matching",
    "semantic search",
    "information retrieval",
    "candidate matching",
]

VECTOR_WORDS = [
    "faiss",
    "pinecone",
    "weaviate",
    "milvus",
    "qdrant",
    "elasticsearch",
    "opensearch",
    "vector database",
    "vector search",
]

EVAL_WORDS = [
    "ndcg",
    "mrr",
    "map",
    "a/b testing",
    "ab testing",
    "offline evaluation",
    "online evaluation",
    "benchmark",
]

LLM_WORDS = [
    "llm",
    "lora",
    "qlora",
    "fine-tuning",
    "peft",
    "transformers",
]

PRODUCTION_WORDS = [
    "production",
    "deployed",
    "deployment",
    "serving",
    "users",
    "scale",
    "pipeline",
    "real users",
    "microservices",
]

PRODUCT_WORDS = [
    "startup",
    "product",
    "0-1",
    "customer",
    "metrics",
    "experimentation",
]


# ===============================
# Generic keyword scorer
# ===============================

def keyword_score(text, words):

    score = 0

    for w in words:
        if w in text:
            score += 1

    return score


# ===============================
# Feature Extraction
# ===============================

def feature_vector(c):

    text = build_candidate_text(c)

    return {
        "retrieval":
            keyword_score(
                text,
                RETRIEVAL_WORDS
            ),

        "vector":
            keyword_score(
                text,
                VECTOR_WORDS
            ),

        "eval":
            keyword_score(
                text,
                EVAL_WORDS
            ),

        "llm":
            keyword_score(
                text,
                LLM_WORDS
            ),

        "production":
            keyword_score(
                text,
                PRODUCTION_WORDS
            ),

        "product":
            keyword_score(
                text,
                PRODUCT_WORDS
            ),
    }