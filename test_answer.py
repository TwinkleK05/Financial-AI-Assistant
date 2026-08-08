from engine.retrieval import retrieve_chunks
from engine.generator import answer_question

question = "What is Apple's market cap?"

chunks = retrieve_chunks(question)

answer = answer_question(
    question,
    chunks
)

print("\nAnswer:\n")
print(answer)