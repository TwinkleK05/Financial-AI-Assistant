from pipeline import *

from engine.vector_store import load_faiss_index

index = load_faiss_index()

print(index.ntotal)

