import requests

BASE_URL = "https://financial-ai-assistant-production.up.railway.app"

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
    chunk_id: str | None = None
):
    """
    Submit user feedback.
    """

    payload = {
        "question": question,
        "chunk_id": chunk_id,
        "rating": rating,
        "comment": comment
    }

    response = requests.post(

        f"{BASE_URL}/feedback",

        json=payload

    )

    response.raise_for_status()

    return response.json()