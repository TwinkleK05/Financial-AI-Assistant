from engine.retrieval import retrieve_chunks
from engine.rbac import authorize_retrieval

question = "What is Apple's market cap?"

chunks = retrieve_chunks(question)

authorized = authorize_retrieval(
    chunks,
    user_role="finance"
)

print(f"Retrieved : {len(chunks)}")
print(f"Authorized: {len(authorized)}")

for chunk in authorized:
    print(chunk.access, "-", chunk.source)