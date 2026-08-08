import json
import logging
from typing import List
from .database import Chunk


import faiss
import numpy as np

from config import (
    FAISS_INDEX_PATH,
    VECTOR_MAPPING_PATH
)

logger = logging.getLogger(__name__)

# ==================================================
# FAISS INDEX
# ==================================================

def build_faiss_index(
    embeddings: np.ndarray
) -> faiss.Index:
    """
    Build a FAISS index from embeddings.
    """

    logger.info("Building FAISS index...")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(
        embeddings.astype(np.float32)
    )

    logger.info(
        f"Indexed {index.ntotal} vectors."
    )

    return index

def save_faiss_index(
    index: faiss.Index
) -> None:
    """
    Save the FAISS index to disk.
    """

    faiss.write_index(
        index,
        str(FAISS_INDEX_PATH)
    )

    logger.info(
        f"FAISS index saved to {FAISS_INDEX_PATH}"
    )

# ==================================================
# VECTOR MAPPING
# ==================================================


def save_vector_mapping(chunks: List[Chunk]) -> None:
    """
    Save the mapping between
    FAISS vector IDs and chunk IDs.
    """

    mapping = {}

    for index, chunk in enumerate(chunks):

        mapping[index] = chunk.id

    with open(
        VECTOR_MAPPING_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            mapping,
            file,
            indent=4
        )

    logger.info(
        f"Saved vector mapping to {VECTOR_MAPPING_PATH}"
    )
    
# ==================================================
# LOAD FAISS
# ==================================================

def load_faiss_index() -> faiss.Index:
    """
    Load the saved FAISS index.
    """

    logger.info("Loading FAISS index...")

    index = faiss.read_index(
        str(FAISS_INDEX_PATH)
    )

    return index

# ==================================================
# LOAD VECTOR MAPPING
# ==================================================
def load_vector_mapping() -> dict[int, str]:
    """
    Load the mapping between
    FAISS vector IDs and chunk IDs.
    """

    logger.info("Loading vector mapping...")

    with open(
        VECTOR_MAPPING_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        mapping = json.load(file)

    # JSON stores keys as strings.
    # Convert them back to integers.
    mapping = {
        int(key): value
        for key, value in mapping.items()
    }

    return mapping