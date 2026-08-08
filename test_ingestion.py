from pipeline import process_uploaded_documents

documents = process_uploaded_documents()

print()

print(f"Total Documents : {len(documents)}")

print()

if documents:

    first = documents[0]

    print(first)

