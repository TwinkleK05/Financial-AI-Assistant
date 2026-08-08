import logging
import json

from typing import List

from .database import Chunk

from config import (
    CHUNKS_FILE,
    METADATA_FILE,
    SUMMARIES_FILE,
)

logger = logging.getLogger(__name__)

# ==================================================
# UNDERSTANDING FILES
# ==================================================

def generate_understanding_files(chunks: List[Chunk]) -> None:
    """
    Generate the semantic understanding files.
    """

    logger.info("Generating understanding files...")

    CHUNKS_FILE.parent.mkdir(parents=True, exist_ok=True)

    chunk_records = []

    metadata_records = []

    summaries = {}

    for chunk in chunks:

        # -------------------------
        # Chunk File
        # -------------------------

        chunk_records.append({

            "chunk_id": chunk.id,

            "document_id": chunk.document_id,

            "text": chunk.text

        })

        # -------------------------
        # Metadata File
        # -------------------------

        metadata_records.append({

            "chunk_id": chunk.id,

            "source": chunk.source,

            "document_type": chunk.document_type,

            "page": chunk.page,

            "sheet": chunk.sheet,

            "row": chunk.row,

            "access": chunk.access

        })

        # -------------------------
        # Summary
        # -------------------------

        if chunk.document_id not in summaries:

            summaries[chunk.document_id] = {

                "document_id": chunk.document_id,

                "source": chunk.source,

                "summary": chunk.text[:300]

            }

    # Save chunks

    with open(CHUNKS_FILE, "w", encoding="utf-8") as file:

        json.dump(

            chunk_records,

            file,

            indent=4

        )

    # Save metadata

    with open(METADATA_FILE, "w", encoding="utf-8") as file:

        json.dump(

            metadata_records,

            file,

            indent=4

        )

    # Save summaries

    with open(SUMMARIES_FILE, "w", encoding="utf-8") as file:

        json.dump(

            list(summaries.values()),

            file,

            indent=4

        )

    logger.info("Understanding files created successfully.")
