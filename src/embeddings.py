from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Model loaded.")

def get_embedding(text):
    return model.encode(
        text,
        normalize_embeddings=True
    )