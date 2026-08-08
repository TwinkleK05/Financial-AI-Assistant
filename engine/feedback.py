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
                chunk_id,
                rating,
                comment
            )
        )

        connection.commit()

        logger.info("Feedback saved.")

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

