import streamlit as st
import pandas as pd
import os

# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Redrob AI Candidate Ranker",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# Header
# ==========================================

st.title("🤖 Redrob AI Candidate Discovery & Ranking System")

st.markdown("""
### Intelligent Candidate Matching using:

✅ Semantic Embeddings

✅ Hybrid Retrieval & Ranking

✅ Career History Analysis

✅ Behavioral Signal Integration

✅ Honeypot Detection

✅ Explainable AI Recommendations
""")

st.markdown("---")

# ==========================================
# Metrics
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Candidates Analysed",
        "100,000"
    )

with col2:
    st.metric(
        "Top Recommendations",
        "100"
    )

with col3:
    st.metric(
        "Embedding Model",
        "MiniLM-L6-v2"
    )

st.markdown("---")

# ==========================================
# JD Input
# ==========================================

jd = st.text_area(
    "Paste Job Description",
    height=300,
    placeholder="Paste the job description here..."
)

# ==========================================
# Find Candidates
# ==========================================

if st.button("🚀 Find Candidates"):

    if jd.strip() == "":
        st.warning("Please paste a Job Description.")
        st.stop()

    st.success("Ranking candidates...")

    if not os.path.exists("submission.csv"):
        st.error(
            "submission.csv not found.\nRun rank.py first."
        )
        st.stop()

    df = pd.read_csv("submission.csv")

    st.markdown("---")
    st.header("🏆 Top Recommended Candidates")

    for _, row in df.head(10).iterrows():

        with st.expander(
            f"🏅 Rank {row['rank']} | {row['candidate_id']}"
        ):

            st.write(
                f"### Candidate ID: {row['candidate_id']}"
            )

            if "score" in df.columns:
                st.write(
                    f"**Final Score:** {row['score']:.3f}"
                )

            st.write(
                f"**Reasoning:**"
            )

            st.info(
                row["reasoning"]
            )

# ==========================================
# Architecture
# ==========================================

st.markdown("---")

st.header("⚙️ System Architecture")

st.code("""
Job Description
        ↓
Sentence Transformer Embeddings
        ↓
Feature Engineering
        ↓
Career Analysis
        ↓
Behavioral Signals
        ↓
Honeypot Detection
        ↓
Hybrid Ranking Engine
        ↓
Top Candidate Recommendations
""")

# ==========================================
# Methodology
# ==========================================

st.markdown("---")

st.header("🧠 Methodology")

st.markdown("""
**1. Semantic Understanding**

The job description and candidate profiles are converted into embeddings using Sentence Transformers.

**2. Feature Engineering**

The system extracts:

- Retrieval experience
- Vector database experience
- LLM expertise
- Production ML experience
- Product engineering experience

**3. Hybrid Scoring**

Final ranking combines:

- Semantic similarity
- Career evidence
- Title priors
- Behavioral signals
- Experience score
- Honeypot penalties

**4. Explainability**

Every recommendation includes reasoning so recruiters understand why a candidate was selected.
""")

# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("📌 System Information")

st.sidebar.success(
    "Hybrid Candidate Ranking System"
)

st.sidebar.write(
    "Dataset Size: 100,000 candidates"
)

st.sidebar.write(
    "Embedding Model: all-MiniLM-L6-v2"
)

st.sidebar.write(
    "Ranking Method: Hybrid Scoring"
)

st.sidebar.write(
    "Output: Top 100 ranked candidates"
)

st.sidebar.markdown("---")

st.sidebar.write(
    "Built for Redrob Intelligent Candidate Discovery & Ranking Challenge"
)