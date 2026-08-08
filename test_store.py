from pipeline import *

initialize_database()

documents = process_uploaded_documents()

chunks = chunk_documents(documents)

store_knowledge(documents, chunks)

print("Knowledge stored successfully!")