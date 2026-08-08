from pipeline import process_uploaded_documents
from pipeline import chunk_documents

documents = process_uploaded_documents()

chunks = chunk_documents(documents)

print()

print(f"Documents : {len(documents)}")

print(f"Chunks : {len(chunks)}")

print()

if chunks:

    print(chunks[0])
