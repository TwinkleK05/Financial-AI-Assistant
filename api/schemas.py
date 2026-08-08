from typing import Optional

from pydantic import BaseModel

# ==================================================
# SOURCES
# ==================================================

class Source(BaseModel):
    """
    Metadata about a retrieved source.
    """

    source: str
    page: Optional[int] = None
    sheet: Optional[str] = None
    row: Optional[int] = None
    access: str
    chunk_id: Optional[str] = None


# ==================================================
# VISUALIZATION
# ==================================================

class ChartPoint(BaseModel):
    """
    A single point in a chart.
    """

    x: str
    y: float


class Visualization(BaseModel):
    """
    Visualization returned by the backend.
    """

    chart_type: str
    title: str
    x_label: str
    y_label: str
    data: list[ChartPoint]


# ==================================================
# ASK
# ==================================================

class AskRequest(BaseModel):
    """
    Request body for asking a question.
    """

    question: str
    role: str


class AskResponse(BaseModel):
    """
    Response returned by the AI Assistant.
    """

    answer: str
    sources: list[Source]
    # Chunks used to build this answer. The frontend echoes these back
    # with feedback so ratings can be tied to the exact retrieved chunks.
    chunk_ids: list[str] = []


# ==================================================
# FEEDBACK
# ==================================================

class FeedbackRequest(BaseModel):
    """
    Request body for submitting user feedback.
    """

    question: str
    chunk_id: Optional[str] = None
    rating: int
    comment: str = ""
    # All chunks that produced the rated answer.
    chunk_ids: Optional[list[str]] = None


class FeedbackResponse(BaseModel):
    """
    Response after feedback is stored.
    """

    message: str


class FeedbackStatsResponse(BaseModel):
    """
    Aggregate view of collected feedback.
    """

    total: int
    average_rating: float
    positive: int
    negative: int
    chunks_with_feedback: int


# ==================================================
# HEALTH
# ==================================================

class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str