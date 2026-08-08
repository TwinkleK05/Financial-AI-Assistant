import logging
from typing import List
import numpy as np

from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL
from .database import Chunk

logger = logging.getLogger(__name__)

# ==================================================
# EMBEDDING MODEL
# ==================================================

_embedding_model = None

def get_embedding_model() -> SentenceTransformer:
    """
    Lazy-load the embedding model.
    The model is loaded only once.
    """

    global _embedding_model

    if _embedding_model is None:

        logger.info("Loading embedding model...")

        _embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    return _embedding_model

# ==================================================
# EMBEDDING GENERATION
# ==================================================

def generate_embeddings(
    chunks: List[Chunk]
) -> np.ndarray:
    """
    Generate embeddings for a list of chunks.
    """

    logger.info("Generating embeddings...")

    model = get_embedding_model()

    texts = [
        chunk.text
        for chunk in chunks
    ]

    embeddings = model.encode(

        texts,

        show_progress_bar=True,

        convert_to_numpy=True,

        normalize_embeddings=True

    )

    logger.info(
        f"Generated embeddings for {len(chunks)} chunks."
    )

    return embeddings

# ==================================================
# QUERY EMBEDDING
# ==================================================

def embed_query(
    question: str
) -> np.ndarray:
    """
    Convert a user question into
    an embedding vector.
    """

    logger.info("Embedding user query...")

    model = get_embedding_model()

    embedding = model.encode(

        question,

        convert_to_numpy=True,

        normalize_embeddings=True

    )

    return embedding.astype(np.float32)
