import logging
import sqlite3

from typing import Optional

from .database import get_connection

logger = logging.getLogger(__name__)


# ==================================================
# SAVE FEEDBACK
# ==================================================

def save_feedback(
    question: str,
    chunk_id: Optional[str],
    rating: int,
    comment: str = ""
) -> None:
    """
    Store user feedback in SQLite.
    """

    logger.info("Saving user feedback...")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Only keep chunk_id if it actually exists
        valid_chunk_id = None

        if chunk_id:
            cursor.execute(
                """
                SELECT 1
                FROM chunks
                WHERE chunk_id = ?
                """,
                (chunk_id,)
            )

            if cursor.fetchone():
                valid_chunk_id = chunk_id
            else:
                logger.warning(
                    f"Chunk '{chunk_id}' not found. "
                    "Saving feedback without chunk_id."
                )

        cursor.execute(
            """
            INSERT INTO feedback(
                question,
                chunk_id,
                rating,
                comment
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                question,
                valid_chunk_id,
                rating,
                comment
            )
        )

        connection.commit()

        logger.info("Feedback saved.")

    except sqlite3.Error as error:
        connection.rollback()
        logger.error(f"Feedback database error: {error}")
        raise

    finally:
        connection.close()


# ==================================================
# READ FEEDBACK
# ==================================================

def get_feedback():
    """
    Return all feedback records.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                question,
                chunk_id,
                rating,
                comment,
                created_at
            FROM feedback
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()