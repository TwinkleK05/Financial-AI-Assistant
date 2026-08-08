from engine.retrieval import retrieve_chunks

question = "What is Apple's market cap?"

chunks = retrieve_chunks(question)

print(f"Retrieved {len(chunks)} chunks\n")

for i, chunk in enumerate(chunks, start=1):
    print("=" * 60)
    print(f"Chunk {i}")
    print("=" * 60)
    print(f"Source : {chunk.source}")
    print(f"Page   : {chunk.page}")
    print(f"Sheet  : {chunk.sheet}")
    print(f"Row    : {chunk.row}")
    print()
    print(chunk.text)
    print()