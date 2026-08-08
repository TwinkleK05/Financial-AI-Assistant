import logging
import sqlite3

from typing import List, Optional

from .database import get_connection

logger = logging.getLogger(__name__)


# ==================================================
# SAVE FEEDBACK
# ==================================================

def save_feedback(
    question: str,
    chunk_id: Optional[str] = None,
    rating: int = 0,
    comment: str = "",
    chunk_ids: Optional[List[str]] = None,
) -> None:
    """
    Store user feedback in SQLite.

    A single answer is usually built from several retrieved chunks.
    To let feedback influence future retrieval, the rating is recorded
    against every chunk that produced the answer: pass them via
    `chunk_ids` (the single `chunk_id` argument is still supported for
    backwards compatibility).

    If no chunk is supplied, one question-level row is stored so the
    feedback is never lost (it just carries no per-chunk signal).
    """

    logger.info("Saving user feedback...")

    # Merge both argument styles into one ordered, de-duplicated list.
    targets: List[str] = []

    for candidate in ([chunk_id] if chunk_id else []) + (chunk_ids or []):
        if candidate and candidate not in targets:
            targets.append(candidate)

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Keep only chunk ids that actually exist (preserve FK integrity).
        valid_targets = []

        for candidate in targets:
            cursor.execute(
                "SELECT 1 FROM chunks WHERE chunk_id = ?",
                (candidate,)
            )

            if cursor.fetchone():
                valid_targets.append(candidate)
            else:
                logger.warning(
                    f"Chunk '{candidate}' not found. "
                    "Skipping chunk association for it."
                )

        # If nothing valid remains, still record the feedback once
        # at the question level (chunk_id = NULL).
        rows = valid_targets if valid_targets else [None]

        for target in rows:
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
                    target,
                    rating,
                    comment
                )
            )

        connection.commit()

        logger.info(
            f"Feedback saved ({len(rows)} row(s))."
        )

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


# ==================================================
# FEEDBACK STATS
# ==================================================

def get_feedback_stats() -> dict:
    """
    Summarise the feedback that drives the retrieval loop.

    Useful for monitoring how much signal the system has learned.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                AVG(rating),
                SUM(CASE WHEN rating >= 4 THEN 1 ELSE 0 END),
                SUM(CASE WHEN rating <= 2 THEN 1 ELSE 0 END),
                COUNT(DISTINCT chunk_id)
            FROM feedback
            """
        )

        row = cursor.fetchone()

        return {
            "total": row[0] or 0,
            "average_rating": round(row[1], 2) if row[1] is not None else 0.0,
            "positive": row[2] or 0,
            "negative": row[3] or 0,
            "chunks_with_feedback": row[4] or 0,
        }

    finally:
        connection.close()