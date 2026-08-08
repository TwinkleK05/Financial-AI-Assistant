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


class FeedbackResponse(BaseModel):
    """
    Response after feedback is stored.
    """

    message: str


# ==================================================
# HEALTH
# ==================================================

class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str