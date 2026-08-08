import logging
import uuid

from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .database import Document, Chunk

from config import CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)

# ==================================================
# TEXT SPLITTER
# ==================================================

def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """
    Returns the configured text splitter.
    """

    return RecursiveCharacterTextSplitter(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP
    )

# ==================================================
# CHUNKING
# ==================================================

def chunk_documents(documents: List[Document]) -> List[Chunk]:
    """
    Convert every document into semantic chunks.
    """

    logger.info("Creating semantic chunks...")

    splitter = get_text_splitter()

    chunks = []

    for document in documents:

        split_text = splitter.split_text(document.text)

        for piece in split_text:

            chunks.append(

                Chunk(

                    id=str(uuid.uuid4()),

                    document_id=document.id,

                    text=piece,

                    source=document.source,

                    document_type=document.document_type,

                    access=document.access,

                    page=document.page,

                    sheet=document.sheet,

                    row=document.row

                )

            )

    logger.info(f"Generated {len(chunks)} chunks.")

    return chunks
