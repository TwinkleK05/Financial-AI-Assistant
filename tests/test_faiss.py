from pipeline import *

from engine.database import get_pending_chunks
chunks = get_pending_chunks()

embeddings = generate_embeddings(chunks)

index = build_faiss_index(embeddings)

save_faiss_index(index)

save_vector_mapping(chunks)

print(index.ntotal)