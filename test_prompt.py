from engine.retrieval import retrieve_chunks
from engine.generator import (
    build_context,
    build_prompt,
)

question = "What is Apple's market cap?"

chunks = retrieve_chunks(question)

context = build_context(chunks)

prompt = build_prompt(
    question,
    context
)

print(prompt)