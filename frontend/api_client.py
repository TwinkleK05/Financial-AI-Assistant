import requests

BASE_URL = "http://127.0.0.1:8000"


# ==================================================
# HEALTH
# ==================================================

def health():
    """
    Check whether the backend is running.
    """

    response = requests.get(
        f"{BASE_URL}/health"
    )

    response.raise_for_status()

    return response.json()


# ==================================================
# ASK
# ==================================================

def ask_question(
    question: str,
    role: str
):
    """
    Send a user question to the backend.
    """

    response = requests.post(

        f"{BASE_URL}/ask",

        json={
            "question": question,
            "role": role
        }

    )

    response.raise_for_status()

    return response.json()


# ==================================================
# FEEDBACK
# ==================================================

def send_feedback(
    question: str,
    rating: int,
    comment: str = "",
    chunk_id: str | None = None,
    chunk_ids: list | None = None
):
    """
    Submit user feedback.

    `chunk_ids` are the chunks that produced the rated answer; sending
    them lets the backend tie the rating to specific retrieved chunks
    and feed it back into future retrieval.
    """

    payload = {
        "question": question,
        "chunk_id": chunk_id,
        "chunk_ids": chunk_ids,
        "rating": rating,
        "comment": comment
    }

    response = requests.post(

        f"{BASE_URL}/feedback",

        json=payload

    )

    response.raise_for_status()

    return response.json()