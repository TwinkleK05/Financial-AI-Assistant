import logging

from fastapi import APIRouter

from .schemas import (
    AskRequest,
    AskResponse,
    FeedbackRequest,
    FeedbackResponse,
    HealthResponse,
    Source,
)

from engine.planner import create_plan
from engine.retrieval import retrieve_chunks
from engine.rbac import authorize_retrieval
from engine.generator import answer_question
from engine.feedback import save_feedback

logger = logging.getLogger(__name__)

router = APIRouter()

# ==================================================
# HEALTH
# ==================================================

@router.get(
    "/health",
    response_model=HealthResponse
)
def health() -> HealthResponse:
    """
    Health check endpoint.
    """

    return HealthResponse(
        status="ok"
    )


# ==================================================
# FEEDBACK
# ==================================================

@router.post(
    "/feedback",
    response_model=FeedbackResponse
)
def feedback(
    request: FeedbackRequest
) -> FeedbackResponse:
    """
    Store user feedback.
    """

    save_feedback(
        question=request.question,
        chunk_id=request.chunk_id,
        rating=request.rating,
        comment=request.comment
    )

    return FeedbackResponse(
        message="Feedback saved."
    )


# ==================================================
# ASK
# ==================================================

@router.post(
    "/ask",
    response_model=AskResponse
)
def ask(
    request: AskRequest
) -> AskResponse:
    """
    Main RAG endpoint.
    """

    logger.info("Received user question.")

    # -----------------------------------------
    # Planning
    # -----------------------------------------

    plan = create_plan(
        request.question
    )

    if not plan.retrieval_required:

        return AskResponse(
            answer="No retrieval was required.",
            sources=[]
        )

    # -----------------------------------------
    # Retrieval
    # -----------------------------------------

    chunks = retrieve_chunks(
        plan.rewritten_question
    )

    logger.info(
        f"Retrieved {len(chunks)} chunks."
    )

    # -----------------------------------------
    # Role-Based Access Control
    # -----------------------------------------

    chunks = authorize_retrieval(
        chunks,
        request.role
    )

    logger.info(
        f"{len(chunks)} chunks remain after RBAC."
    )

    if not chunks:

        return AskResponse(
            answer="You do not have permission to access any relevant documents.",
            sources=[]
        )

    # -----------------------------------------
    # Answer Generation
    # -----------------------------------------

    answer = answer_question(
        plan.rewritten_question,
        chunks
    )

    # -----------------------------------------
    # Sources
    # -----------------------------------------

    sources = []

    for chunk in chunks:

        sources.append(

            Source(
                source=chunk.source,
                page=chunk.page,
                sheet=chunk.sheet,
                row=chunk.row,
                access=chunk.access,
            )

        )

    logger.info("Returning response.")

    return AskResponse(

        answer=answer,

        sources=sources

    )