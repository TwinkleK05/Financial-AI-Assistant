"""
Unit tests for the feedback re-ranking loop.

These exercise the pure ranking logic (no FAISS / embedding model
required) so they can run anywhere:

    python tests/test_feedback_loop.py
"""

import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from engine.database import Chunk
from engine.feedback_ranker import (
    rating_to_signal,
    blend_and_rank,
)


def make_chunk(chunk_id: str) -> Chunk:
    return Chunk(
        id=chunk_id,
        document_id="doc",
        text=f"text-{chunk_id}",
        source="file.xlsx",
        document_type="excel",
        access="public",
    )


# ==================================================
# rating_to_signal
# ==================================================

def test_rating_to_signal():

    assert rating_to_signal(5) == 1.0
    assert rating_to_signal(4) == 0.5
    assert rating_to_signal(3) == 0.0
    assert rating_to_signal(1) == -1.0

    # Out-of-range ratings stay clamped to [-1, 1].
    assert rating_to_signal(10) == 1.0
    assert rating_to_signal(-5) == -1.0

    print("rating_to_signal ....................... OK")


# ==================================================
# blend_and_rank
# ==================================================

def test_no_feedback_preserves_semantic_order():

    a, b, c = make_chunk("a"), make_chunk("b"), make_chunk("c")

    scored = [(a, 0.9), (b, 0.8), (c, 0.7)]

    ranked = blend_and_rank(scored, boosts={}, weight=0.15, top_k=2)

    assert [chunk.id for chunk in ranked] == ["a", "b"]

    print("no-feedback order preserved ............ OK")


def test_positive_feedback_promotes_chunk():

    # Semantically, "c" is last. A strong upvote (boost 1.0 * weight
    # 0.15 = +0.15) lifts it from 0.70 to 0.85 — past "b" (0.80) but
    # not past "a" (0.90) — so it enters the top-2 in second place.
    a, b, c = make_chunk("a"), make_chunk("b"), make_chunk("c")

    scored = [(a, 0.90), (b, 0.80), (c, 0.70)]

    boosts = {"c": 1.0}  # e.g. accumulated helpful feedback

    ranked = blend_and_rank(scored, boosts, weight=0.15, top_k=2)

    ids = [chunk.id for chunk in ranked]

    assert "c" in ids, f"expected 'c' promoted, got {ids}"
    assert "b" not in ids, f"expected 'b' displaced, got {ids}"
    assert ids == ["a", "c"], f"unexpected order {ids}"

    print("positive feedback promotes chunk ....... OK")


def test_negative_feedback_demotes_chunk():

    # "a" is top semantically but was repeatedly marked unhelpful.
    a, b, c = make_chunk("a"), make_chunk("b"), make_chunk("c")

    scored = [(a, 0.90), (b, 0.85), (c, 0.84)]

    boosts = {"a": -1.0}

    ranked = blend_and_rank(scored, boosts, weight=0.15, top_k=2)

    ids = [chunk.id for chunk in ranked]

    assert ids == ["b", "c"], f"expected 'a' demoted, got {ids}"

    print("negative feedback demotes chunk ........ OK")


def test_weight_bounds_influence():

    # A tiny weight must NOT let feedback override a clear semantic gap.
    a, b = make_chunk("a"), make_chunk("b")

    scored = [(a, 0.90), (b, 0.50)]

    ranked = blend_and_rank(scored, {"b": 1.0}, weight=0.15, top_k=1)

    assert [chunk.id for chunk in ranked] == ["a"]

    print("weight bounds feedback influence ....... OK")


if __name__ == "__main__":

    test_rating_to_signal()
    test_no_feedback_preserves_semantic_order()
    test_positive_feedback_promotes_chunk()
    test_negative_feedback_demotes_chunk()
    test_weight_bounds_influence()

    print("\nAll feedback-loop tests passed.")
