"""
Financial AI Assistant Pipeline

Acts as the orchestration layer.

Every feature is implemented inside
the engine package.
"""

from engine.ingestion import process_uploaded_documents
from engine.chunking import chunk_documents
from engine.database import (
    initialize_database,
    store_knowledge,
)
from engine.embeddings import generate_embeddings
from engine.vector_store import (
    build_faiss_index,
    save_faiss_index,
    save_vector_mapping,
)
from engine.understanding import generate_understanding_files

import logging

logger = logging.getLogger(__name__)

def build_knowledge_base() -> tuple:
    logger.info("Starting knowledge base pipeline...")
    initialize_database()

    documents = process_uploaded_documents()

    chunks = chunk_documents(documents)

    store_knowledge(documents, chunks)

    embeddings = generate_embeddings(chunks)

    index = build_faiss_index(embeddings)

    save_faiss_index(index)

    save_vector_mapping(chunks)

    generate_understanding_files(chunks)

    logger.info("Knowledge base pipeline completed.")

    return documents, chunks, embeddings, index