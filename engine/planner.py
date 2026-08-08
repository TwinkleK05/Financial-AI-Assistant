import logging

from dataclasses import dataclass

logger = logging.getLogger(__name__)


# ==================================================
# PLANNER RESULT
# ==================================================

@dataclass
class PlannerResult:
    """
    Represents the execution plan
    for a user question.
    """

    original_question: str

    rewritten_question: str

    retrieval_required: bool

# ==================================================
# QUESTION CLEANING
# ==================================================

def clean_question(
    question: str
) -> str:
    """
    Normalize a user question before retrieval.
    """

    logger.info("Cleaning user question...")

    cleaned = " ".join(
        question.strip().split()
    )

    return cleaned

# ==================================================
# RETRIEVAL DECISION
# ==================================================

def needs_retrieval(
    question: str
) -> bool:
    """
    Decide whether the question
    requires knowledge retrieval.

    Current implementation always
    returns True.
    """

    logger.info("Determining retrieval requirement...")

    return True

# ==================================================
# PLANNER
# ==================================================

def create_plan(
    question: str
) -> PlannerResult:
    """
    Create an execution plan
    for the user question.
    """

    logger.info("Creating execution plan...")

    cleaned_question = clean_question(
        question
    )

    retrieval_required = needs_retrieval(
        cleaned_question
    )

    plan = PlannerResult(

        original_question=question,

        rewritten_question=cleaned_question,

        retrieval_required=retrieval_required

    )

    logger.info("Execution plan created.")

    return plan

