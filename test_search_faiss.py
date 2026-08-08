from pipeline import *
from test_query_embedding import search_faiss

from engine.embeddings import embed_query

embedding = embed_query(
    "What was Apple's revenue?"
)

scores, indices = search_faiss(
    embedding
)

print(scores)

print(indices)