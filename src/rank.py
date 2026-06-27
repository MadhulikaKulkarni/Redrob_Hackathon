import os
import subprocess
import numpy as np
import pandas as pd

from load_data import load_candidates
from embeddings import get_embedding
from feature_engineering import feature_vector
from scoring import final_score
from sklearn.metrics.pairwise import cosine_similarity
from reasoning import generate_reasoning


print("Loading candidates...")
candidates = load_candidates()

if not os.path.exists("candidate_embeddings.npy"):
    print("Embeddings not found.")
    print("Generating embeddings...")
    subprocess.run(
        ["python", "src/precompute_embeddings.py"],
        check=True
    )

print("Loading precomputed embeddings...")
candidate_embeddings = np.load(
    "candidate_embeddings.npy"
)

print("Loading Job Description...")
with open(
    "data/job_description.txt",
    "r",
    encoding="utf8"
) as f:
    jd = f.read()

print("Creating JD embedding...")
jd_embedding = get_embedding(jd)

scores = []

print("Ranking candidates...")

for i, c in enumerate(candidates):

    if i % 10000 == 0:
        print(f"Processed {i} candidates...")

    similarity = cosine_similarity(
        [jd_embedding],
        [candidate_embeddings[i]]
    )[0][0]

    features = feature_vector(c)

    score = final_score(
        similarity,
        features,
        c
    )

    scores.append(
        (
            score,
            c
        )
    )

print("Sorting candidates...")

scores.sort(
    key=lambda x: x[0],
    reverse=True
)

print("\nTOP 20\n")

for score, c in scores[:20]:
    print(
        round(score, 3),
        c["candidate_id"],
        c["profile"]["current_title"]
    )

rows = []

for rank, (score, c) in enumerate(
        scores[:100],
        start=1
):

    rows.append(
        {
            "candidate_id":
                c["candidate_id"],

            "rank":
                rank,

            "score":
                round(float(score), 6),

            "reasoning":
                generate_reasoning(
                    c,
                    feature_vector(c)
                 )
        }
    )

df = pd.DataFrame(rows)

df.to_csv(
    "submission.csv",
    index=False
)

print("\nsubmission.csv created.")
