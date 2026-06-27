import numpy as np

from load_data import load_candidates
from feature_engineering import (
    build_candidate_text
)
from embeddings import model

print("Loading candidates...")

candidates = load_candidates()

texts = []

for c in candidates:
    texts.append(
        build_candidate_text(c)
    )

print(
    "Creating embeddings..."
)

embeddings = model.encode(
    texts,
    batch_size=128,
    show_progress_bar=True,
    normalize_embeddings=True
)

np.save(
    "candidate_embeddings.npy",
    embeddings
)

print(
    "Saved:",
    embeddings.shape
)