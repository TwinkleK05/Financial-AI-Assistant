from pipeline import process_uploaded_documents
from pipeline import chunk_documents
from pipeline import generate_understanding_files

documents = process_uploaded_documents()

chunks = chunk_documents(documents)

generate_understanding_files(chunks)

print("Understanding files generated!")