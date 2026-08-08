import logging
import numpy as np

from typing import List

from config import TOP_K_RESULTS

from .database import (
    Chunk,
    get_connection,
)

from .embeddings import embed_query

from .vector_store import (
    load_faiss_index,
    load_vector_mapping,
)

logger = logging.getLogger(__name__)

# ==================================================
# SEMANTIC SEARCH
# ==================================================

def search_faiss(
    query_embedding: np.ndarray,
    top_k: int = 5
) -> tuple[np.ndarray, np.ndarray]:
    """
    Search the FAISS index and return
    similarity scores and vector indices.
    """

    logger.info("Searching FAISS index...")

    index = load_faiss_index()

    scores, indices = index.search(

        query_embedding.reshape(1, -1),

        top_k

    )

    return scores[0], indices[0]

def fetch_chunk(chunk_id: str) -> Chunk:
    """
    Retrieve one chunk from SQLite
    using its chunk ID.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            c.chunk_id,

            c.document_id,

            c.text,

            m.page,

            m.sheet,

            m.row,

            m.access,

            d.source,

            d.document_type

        FROM chunks c

        JOIN metadata m

        ON c.chunk_id = m.chunk_id

        JOIN documents d

        ON c.document_id = d.document_id

        WHERE c.chunk_id = ?
        """,
        (chunk_id,)
    )

    try:
        row = cursor.fetchone()
    finally:
        connection.close()


    if row is None:
        raise ValueError(f"Chunk '{chunk_id}' not found.")

    logger.debug(f"Fetched chunk: {chunk_id}")

    return Chunk(
        id=row[0],
        document_id=row[1],
        text=row[2],
        page=row[3],
        sheet=row[4],
        row=row[5],
        access=row[6],
        source=row[7],
        document_type=row[8]
    )

def retrieve_chunks(
    question: str,
    top_k: int = TOP_K_RESULTS
) -> List[Chunk]:
    """
    Retrieve the most relevant chunks
    for a user question.
    """

    logger.info("Retrieving relevant chunks...")

    query_embedding = embed_query(question)

    _, indices = search_faiss(
        query_embedding,
        top_k
    )
    mapping = load_vector_mapping()
 
    retrieved_chunks = []

    for index in indices:

        if index == -1:
            continue

        chunk_id = mapping.get(index)

        if chunk_id is None:
            continue

        chunk = fetch_chunk(chunk_id)

        retrieved_chunks.append(chunk)

    if not retrieved_chunks:
        logger.warning("No relevant chunks were retrieved.")

    logger.info(
        f"Retrieved {len(retrieved_chunks)} chunks."
    )
    
    return retrieved_chunks

