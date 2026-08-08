from engine.retrieval import retrieve_chunks
from engine.generator import build_context

chunks = retrieve_chunks(
    "What is Apple's market cap?"
)

context = build_context(chunks)

print(context)