from pipeline import *

from engine.embeddings import embed_query

embedding = embed_query(
    "What was Apple's revenue?"
)

print(embedding.shape)

print(embedding.dtype)

