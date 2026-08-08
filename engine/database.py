
import logging
import sqlite3

from dataclasses import dataclass
from typing import List, Optional


from config import DATABASE_PATH

logger = logging.getLogger(__name__)

# ==========================================================
# DATA MODEL
# ==========================================================

@dataclass
class Document:
    """
    Represents a normalized document inside the RAG pipeline.
    Every PDF page and every Excel row is converted into this format.
    """

    id: str

    text: str

    source: str

    document_type: str

    access: str

    page: Optional[int] = None

    sheet: Optional[str] = None

    row: Optional[int] = None

# ==================================================
# CHUNK MODEL
# ==================================================

@dataclass
class Chunk:
    """
    Represents one semantic chunk generated
    from a document.
    """

    id: str

    document_id: str

    text: str

    source: str

    document_type: str

    access: str

    page: Optional[int] = None

    sheet: Optional[str] = None

    row: Optional[int] = None

# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite connection.
    """

    connection = sqlite3.connect(str(DATABASE_PATH))

    connection.execute("PRAGMA foreign_keys = ON")

    return connection

# ==================================================
# DATABASE INITIALIZATION
# ==================================================

def initialize_database() -> None:
    """
    Create all required tables.
    Safe to call multiple times.
    """

    logger.info("Initializing SQLite database...")

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------
    # Documents
    # --------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        document_id TEXT PRIMARY KEY,

        source TEXT NOT NULL,

        document_type TEXT NOT NULL,

        access TEXT NOT NULL,

        page_count INTEGER,

        summary TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # --------------------------------------------------
    # Chunks
    # --------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (

        chunk_id TEXT PRIMARY KEY,

        document_id TEXT NOT NULL,

        text TEXT NOT NULL,

        embedding_status TEXT DEFAULT 'pending',

        FOREIGN KEY(document_id)
         REFERENCES documents(document_id)

    )
    """)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metadata (

        chunk_id TEXT PRIMARY KEY,

        document_id TEXT NOT NULL,

        page INTEGER,

        sheet TEXT,

        row INTEGER,

        access TEXT,

        FOREIGN KEY(chunk_id)
        REFERENCES chunks(chunk_id),

        FOREIGN KEY(document_id)
        REFERENCES documents(document_id)

    )
    """)

    # --------------------------------------------------
    # Feedback
    # --------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        question TEXT,

        chunk_id TEXT,

        rating INTEGER,

        comment TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(chunk_id)
        REFERENCES chunks(chunk_id)

    )
    """)
    try:
        connection.commit()
    finally:
        connection.close()

    logger.info("Database initialized.")

# ==================================================
# DOCUMENT REPOSITORY
# ==================================================

def save_document(
    connection: sqlite3.Connection,
    document: Document
) -> None:
    """
    Save one document inside the documents table.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO documents(

            document_id,

            source,

            document_type,

            access,

            page_count,

            summary

        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,

        (

            document.id,

            document.source,

            document.document_type,

            document.access,

            None,

            None

        )

    )
# ==================================================
# CHUNK REPOSITORY
# ==================================================

def save_chunk(
    connection: sqlite3.Connection,
    chunk: Chunk
) -> None:
    """
    Save one semantic chunk into the database.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO chunks(

            chunk_id,

            document_id,

            text,

            embedding_status

        )

        VALUES (?, ?, ?, ?)
        """,

        (

            chunk.id,

            chunk.document_id,

            chunk.text,

            "pending"

        )

    )
# ==================================================
# METADATA REPOSITORY
# ==================================================

def save_metadata(
    connection: sqlite3.Connection,
    chunk: Chunk
) -> None:
    """
    Save metadata associated with a chunk.
    """

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO metadata(

            chunk_id,

            document_id,

            page,

            sheet,

            row,

            access

        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,

        (

            chunk.id,

            chunk.document_id,

            chunk.page,

            chunk.sheet,

            chunk.row,

            chunk.access

        )

    )

# ==================================================
# KNOWLEDGE STORE
# ==================================================

def store_knowledge(
    documents: List[Document],
    chunks: List[Chunk]
) -> None:
    """
    Persist all documents and chunks
    into the SQLite knowledge store.
    """

    logger.info("Saving knowledge into SQLite...")

    connection = get_connection()

    try:

        for document in documents:

            save_document(
                connection,
                document
            )

        for chunk in chunks:

            save_chunk(
                connection,
                chunk
            )

            save_metadata(
                connection,
                chunk
            )

        connection.commit()

        logger.info("Knowledge stored successfully.")

    except Exception as error:

        connection.rollback()

        logger.error(f"Database error: {error}")

        raise

    finally:

        connection.close()

# ==================================================
# READ PENDING CHUNKS
# ==================================================

def get_pending_chunks() -> List[Chunk]:
    """
    Return all chunks waiting
    for embedding generation.
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

        WHERE c.embedding_status='pending'
        """
    )

    try:
       rows = cursor.fetchall()
    finally:
       connection.close()

    chunks = []

    for row in rows:

        chunks.append(

            Chunk(

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

        )

    return chunks
