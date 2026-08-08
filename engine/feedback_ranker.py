"""
feedback_ranker.py

Closes the retrieval feedback loop.

User feedback is stored in SQLite (question, chunk_id, rating).
This module turns that history into a per-chunk signal and uses it
to re-rank the semantic search results before they reach the LLM.

The signal is *question-aware*: feedback given on one question only
influences a new question if the two are semantically similar. This
prevents a chunk that was great for "Apple's market cap" from being
promoted for an unrelated question about, say, leadership history.

Design notes
------------
* FAISS uses inner product over normalised embeddings, so semantic
  scores are cosine similarities in ~[0, 1].
* Each rating is mapped to a signal in [-1, 1] (see `rating_to_signal`).
* A chunk's boost is the similarity-weighted sum of the signals from
  matching feedback, clamped to [-1, 1].
* Final score = semantic_score + FEEDBACK_WEIGHT * boost.

Everything here is defensive: if feedback can't be read or embedded,
retrieval silently falls back to pure semantic ranking.
"""

import logging

from typing import Dict, List, Optional, Tuple

import numpy as np

from config import (
    FEEDBACK_SIMILARITY_THRESHOLD,
    FEEDBACK_WEIGHT,
    TOP_K_RESULTS,
)

from .database import Chunk, get_connection

logger = logging.getLogger(__name__)

# A (chunk, semantic_score) pair produced by semantic search.
ScoredChunk = Tuple[Chunk, float]

# Cache of feedback-question embeddings so repeated queries don't
# re-encode the same past questions. Keyed by the raw question text.
_question_embedding_cache: Dict[str, np.ndarray] = {}


# ==================================================
# RATING -> SIGNAL
# ==================================================

def rating_to_signal(rating: int) -> float:
    """
    Map a 1-5 rating onto a [-1, 1] signal centred on 3.

        5 -> +1.0   (very helpful)
        4 -> +0.5
        3 ->  0.0   (neutral)
        1 -> -1.0   (not helpful)

    A "helpful" thumbs-up (rating 5) and a "not helpful"
    thumbs-down (rating 1) therefore pull symmetrically.
    """

    signal = (float(rating) - 3.0) / 2.0

    return max(-1.0, min(1.0, signal))


# ==================================================
# LOAD FEEDBACK
# ==================================================

def load_feedback_rows() -> List[Tuple[str, str, int]]:
    """
    Return usable feedback rows as (question, chunk_id, rating).

    Rows without a chunk_id or rating carry no learnable signal
    for re-ranking, so they are skipped here (they still live in
    the feedback table for analytics).
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT question, chunk_id, rating
            FROM feedback
            WHERE chunk_id IS NOT NULL
              AND rating IS NOT NULL
              AND question IS NOT NULL
            """
        )

        return [
            (row[0], row[1], int(row[2]))
            for row in cursor.fetchall()
        ]

    finally:
        connection.close()


# ==================================================
# EMBED PAST QUESTIONS
# ==================================================

def embed_questions(questions: List[str]) -> Dict[str, np.ndarray]:
    """
    Return a {question: normalised embedding} map for the given
    questions, encoding only the ones not already cached.

    The embedding model is imported lazily so this module stays
    importable (and unit-testable) without the heavy ML stack.
    """

    missing = [
        question
        for question in questions
        if question not in _question_embedding_cache
    ]

    if missing:

        # Local import keeps sentence-transformers out of module load.
        from .embeddings import get_embedding_model

        model = get_embedding_model()

        vectors = model.encode(
            missing,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        for question, vector in zip(missing, vectors):
            _question_embedding_cache[question] = vector.astype(np.float32)

    return {
        question: _question_embedding_cache[question]
        for question in questions
        if question in _question_embedding_cache
    }


# ==================================================
# COMPUTE BOOSTS
# ==================================================

def compute_boosts(
    query_embedding: np.ndarray,
    feedback_rows: List[Tuple[str, str, int]],
    candidate_ids: set,
    threshold: float = FEEDBACK_SIMILARITY_THRESHOLD,
) -> Dict[str, float]:
    """
    Compute a feedback boost in [-1, 1] for each candidate chunk.

    For every feedback row whose chunk is among the candidates and
    whose question is similar enough to the current one, the chunk
    accumulates `similarity * rating_signal`. The result is clamped.
    """

    # Only feedback about chunks we are actually ranking matters.
    relevant = [
        (question, chunk_id, rating)
        for (question, chunk_id, rating) in feedback_rows
        if chunk_id in candidate_ids
    ]

    if not relevant:
        return {}

    distinct_questions = list({question for question, _, _ in relevant})

    question_vectors = embed_questions(distinct_questions)

    query_vector = np.asarray(query_embedding, dtype=np.float32)

    boosts: Dict[str, float] = {}

    for question, chunk_id, rating in relevant:

        past_vector = question_vectors.get(question)

        if past_vector is None:
            continue

        # Both vectors are normalised, so dot product == cosine.
        similarity = float(np.dot(query_vector, past_vector))

        if similarity < threshold:
            continue

        boosts[chunk_id] = (
            boosts.get(chunk_id, 0.0)
            + similarity * rating_to_signal(rating)
        )

    # Clamp so no single chunk can be boosted without bound.
    for chunk_id in boosts:
        boosts[chunk_id] = max(-1.0, min(1.0, boosts[chunk_id]))

    return boosts


# ==================================================
# BLEND AND RANK
# ==================================================

def blend_and_rank(
    scored_chunks: List[ScoredChunk],
    boosts: Dict[str, float],
    weight: float = FEEDBACK_WEIGHT,
    top_k: Optional[int] = TOP_K_RESULTS,
) -> List[Chunk]:
    """
    Re-rank chunks by `semantic_score + weight * boost` and return
    the top-k chunks.

    `sorted` is stable, so chunks with no feedback keep their original
    semantic ordering — with an empty `boosts` map this is a no-op
    that simply trims to top-k.
    """

    ranked = sorted(
        scored_chunks,
        key=lambda pair: pair[1] + weight * boosts.get(pair[0].id, 0.0),
        reverse=True,
    )

    if top_k is not None:
        ranked = ranked[:top_k]

    return [chunk for chunk, _ in ranked]


# ==================================================
# RE-RANK BY FEEDBACK (ORCHESTRATION)
# ==================================================

def rerank_by_feedback(
    query_embedding: np.ndarray,
    scored_chunks: List[ScoredChunk],
    top_k: int = TOP_K_RESULTS,
    weight: float = FEEDBACK_WEIGHT,
    threshold: float = FEEDBACK_SIMILARITY_THRESHOLD,
) -> List[Chunk]:
    """
    Apply the feedback loop to semantic search results.

    Falls back to pure semantic ranking (just trimmed to top-k) if
    there is no usable feedback or anything goes wrong reading it.
    """

    if not scored_chunks:
        return []

    try:
        feedback_rows = load_feedback_rows()
    except Exception as error:
        logger.warning(f"Could not load feedback for re-ranking: {error}")
        feedback_rows = []

    if not feedback_rows:
        return [chunk for chunk, _ in scored_chunks[:top_k]]

    candidate_ids = {chunk.id for chunk, _ in scored_chunks}

    try:
        boosts = compute_boosts(
            query_embedding,
            feedback_rows,
            candidate_ids,
            threshold,
        )
    except Exception as error:
        logger.warning(f"Feedback boost computation failed: {error}")
        boosts = {}

    if not boosts:
        return [chunk for chunk, _ in scored_chunks[:top_k]]

    logger.info(
        f"Applying feedback re-ranking to {len(boosts)} of "
        f"{len(scored_chunks)} candidate chunks."
    )

    return blend_and_rank(scored_chunks, boosts, weight, top_k)
