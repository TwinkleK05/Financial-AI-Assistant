import logging

from typing import List

from groq import Groq

from config import (
    GROQ_API_KEY,
    LLM_MODEL,
)

from .database import Chunk

logger = logging.getLogger(__name__)

# ==================================================
# SYSTEM PROMPT
# ==================================================

SYSTEM_PROMPT = """
You are Financial AI Assistant, an experienced enterprise financial analyst.

Your purpose is to answer questions like an experienced enterprise financial analyst.

Your responses should feel natural, professional, and conversational.

Do not sound like a search engine, database, or document reader.

Your responses should sound like a knowledgeable human financial analyst,
not like a database or search engine.

Follow these principles:

Carefully read all retrieved documents before answering.

Synthesize information from all relevant documents into one coherent response instead of answering from each document separately.

• Write naturally and conversationally.

• Be concise but informative.

• Never simply copy the retrieved text.

• Synthesize information from multiple documents whenever possible.

If multiple records answer the question:

• Identify why multiple values exist (different years, companies, quarters, etc.).

• Explain that naturally.

• Then present the values in a clean markdown table whenever appropriate.

• If trends are visible,
  briefly mention them.

Only explain financial concepts when the user explicitly asks for a definition or explanation.

Examples:

"What is EBITDA?"

"What is market capitalization?"

"Explain stock price."

Do NOT explain financial concepts when the user asks for a specific value.

Examples:

"What is Apple's market cap?"

"What was Google's stock price?"

These questions should be answered directly.

• When comparing values,
  use markdown tables whenever appropriate.

• Never invent numerical values.

• Never fabricate companies or financial metrics.

• If the retrieved documents do not contain enough information,
  clearly say:

"I could not find the answer in the provided documents."

Never describe your reasoning process.

Never say:

"To answer the question..."

"Based on the retrieved documents..."

"We need to..."

"Looking at the provided documents..."

Instead, immediately answer the user's question naturally.

Write as if you are talking to a colleague.

Avoid sounding like an AI assistant.

Avoid unnecessary introductions.

Do not repeat the user's question.

Start with the answer immediately.

When numerical values are involved:

• Use markdown tables whenever they improve readability.

• Round only if the source already rounds the value.

• Preserve the original numerical values from the documents.


Your goal is to provide answers that feel helpful,
professional,
clear,
and easy to read.
"""

# ==================================================
# GROQ CLIENT
# ==================================================

groq_client = None


# ==================================================
# LOAD MODEL
# ==================================================

def get_llm() -> Groq:
    """
    Lazy-load the Groq client.
    """

    global groq_client

    if groq_client is None:

        logger.info("Loading Groq client...")

        groq_client = Groq(
            api_key=GROQ_API_KEY
        )

    return groq_client


# ==================================================
# BUILD CONTEXT
# ==================================================

def build_context(
    chunks: List[Chunk]
) -> str:
    """
    Convert retrieved chunks into a
    structured context for the LLM.
    """

    logger.info("Building retrieval context...")

    sections = []

    for i, chunk in enumerate(chunks, start=1):

        formatted_text = (
            chunk.text
            .replace("|", "\n")
            .strip()
        )

        sections.append(
            f"""
==================================================
DOCUMENT {i}
==================================================

Metadata

Source File : {chunk.source}

Access Level : {chunk.access}

Sheet : {chunk.sheet}

Page : {chunk.page}

Row : {chunk.row}

--------------------------------------------------

Financial Information

{formatted_text}

"""
        )

    return "\n".join(sections)

# ==================================================
# BUILD PROMPT
# ==================================================

def build_prompt(
    question: str,
    context: str
) -> str:
    """
    Build the prompt that will be
    sent to the LLM.
    """

    logger.info("Building prompt...")

    return f"""
Below are the retrieved enterprise financial documents.

Use ONLY these documents to answer the user's question.

------------------------------
RETRIEVED DOCUMENTS
------------------------------

{context}

------------------------------
USER QUESTION
------------------------------

{question}

------------------------------
YOUR TASK
------------------------------

Before answering:

1. Read every retrieved document carefully.

2. Understand what the user is actually asking.

3. Combine information from multiple documents whenever appropriate.

4. Do not simply repeat the retrieved records.

5. Produce one natural answer.

If multiple values exist:

• Organize them logically.

• Mention why multiple values exist.

• Present them chronologically whenever possible.

If the question asks for a comparison:

• Compare the information clearly.

• Use markdown tables whenever appropriate.

If the question asks for a definition:

• Explain the concept first.

• Then relate it to the retrieved financial documents.

If the retrieved documents do not contain enough information,
reply naturally.

Example:

"I couldn't find information about that in the available financial documents."

Do not invent missing information.

------------------------------
FINAL ANSWER
------------------------------
"""


# ==================================================
# GENERATE ANSWER
# ==================================================

def generate_answer(
    prompt: str
) -> str:
    """
    Generate an answer using Groq.
    """

    logger.info("Generating answer...")

    client = get_llm()

    response = client.chat.completions.create(

        model=LLM_MODEL,

        temperature=0.4,

        max_tokens=1024,

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    return response.choices[0].message.content.strip()


# ==================================================
# QUESTION ANSWERING
# ==================================================

def answer_question(
    question: str,
    chunks: List[Chunk]
) -> str:
    """
    Generate the final answer
    from retrieved chunks.
    """

    logger.info("Generating final answer...")

    if not chunks:

        return (
            "I could not find the answer in the "
            "provided documents."
        )

    context = build_context(
        chunks
    )

    prompt = build_prompt(
        question,
        context
    )

    answer = generate_answer(
        prompt
    )

    return answer