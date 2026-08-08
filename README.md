# Enterprise Financial AI Assistant

## Overview

Enterprise Financial AI Assistant is a Retrieval-Augmented Generation (RAG) system designed to enable secure and intelligent querying of enterprise financial documents using natural language.

The application combines semantic search, Large Language Models (LLMs), and role-based access control to generate accurate, context-aware responses grounded in organizational data rather than relying on the model's internal knowledge.

Instead of asking users to manually search through spreadsheets or reports, the assistant retrieves relevant financial information from enterprise documents and synthesizes it into concise, human-readable responses while providing complete source attribution.

The system is built with a modular architecture consisting of a FastAPI backend, a Streamlit frontend, a FAISS vector database for semantic retrieval, SQLite for metadata and feedback storage, and Groq-hosted LLMs for response generation.

---

# Key Features

## Retrieval-Augmented Generation (RAG)

Implements a complete Retrieval-Augmented Generation pipeline where retrieved enterprise documents are used as context before generating responses.

This minimizes hallucinations and ensures that answers remain grounded in the organization's financial knowledge base.

---

## Natural Language Financial Question Answering

Users can ask questions in natural language such as:

- What was Apple's stock price in 2007?
- Compare Google's market capitalization over the years.
- Explain EBITDA.
- Which company had the highest revenue?
- Show Microsoft's financial metrics.

The assistant automatically retrieves relevant documents before generating the response.

---

## Enterprise Document Search

Supports retrieval from enterprise financial documents including:

- PDF Reports
- Excel Workbooks

Semantic search enables users to retrieve information even when exact keywords are not present.

---

## Role-Based Access Control (RBAC)

The system enforces document-level authorization.

Supported roles include:

- CEO
- Finance
- CTO
- Intern

Before response generation, retrieved documents are filtered according to the user's role to ensure unauthorized information never reaches the language model.

---

## Source Attribution

Every generated response includes references to the supporting documents.

Displayed metadata includes:

- Source File
- Sheet Name
- Page Number
- Row Number
- Access Level

This improves transparency and allows users to verify the generated answers.

---

## Feedback Loop

Users can provide feedback on generated responses, and that feedback is fed back into retrieval — closing the loop rather than just collecting data.

The application stores, for every rated answer:

- Question
- The chunks that produced the answer
- Rating
- Comment
- Timestamp

At retrieval time the system:

1. Pulls a larger candidate pool from the FAISS index.
2. Converts past ratings into a per-chunk signal, weighted by how semantically similar the current question is to the question that was originally rated (so feedback on one topic does not leak into unrelated queries).
3. Re-ranks the candidates by blending semantic similarity with this feedback signal before passing the top results to the LLM.

The effect is that chunks which previously produced good answers are promoted, and chunks that produced poor answers are demoted, for semantically similar future questions. The behaviour is fully configurable (and can be switched off) in `config.py`.

---

## Enterprise User Interface

The Streamlit frontend provides:

- Conversational chat interface
- Role selection
- Backend health monitoring
- Source references
- Feedback collection
- Responsive layout

---

# System Architecture

```
                                   Enterprise Financial Documents
                                (PDF Reports / Excel Workbooks)
                                                │
                                                ▼
                                    Document Processing Pipeline
                                                │
                         ┌──────────────────────┴──────────────────────┐
                         │                                             │
                         ▼                                             ▼
                 Text Extraction                               Metadata Extraction
                         │                                             │
                         └──────────────────────┬──────────────────────┘
                                                ▼
                                        Text Chunking
                                                │
                                                ▼
                               Sentence Transformer Embeddings
                                                │
                                                ▼
                                     FAISS Vector Database
                                                │
──────────────────────────────────────────────────────────────────────────────────────────
                                            Runtime Pipeline
──────────────────────────────────────────────────────────────────────────────────────────

                                         User Question
                                                │
                                                ▼
                                         Query Planner
                                                │
                                                ▼
                                   Query Normalization
                                                │
                                                ▼
                                   Semantic Vector Search
                                                │
                                                ▼
                                   Top-K Relevant Chunks
                                                │
                                                ▼
                                Role-Based Access Control
                                                │
                                                ▼
                                       Context Builder
                                                │
                                                ▼
                                  Prompt Construction
                                                │
                                                ▼
                              Groq Large Language Model
                                                │
                                                ▼
                                Response Generation
                                                │
                                                ▼
                             Source Metadata Attachment
                                                │
                                                ▼
                                  Streamlit Frontend
                                                │
                                                ▼
                               User Feedback Collection
                                                │
                                                ▼
                                   SQLite Feedback Store
```

---

# Retrieval Pipeline

The assistant follows a Retrieval-Augmented Generation workflow to ensure responses remain grounded in enterprise documents.

### Step 1 — User Query

The user submits a natural language question through the Streamlit interface.

Example:

```
What was Apple's stock price in 2007?
```

---

### Step 2 — Query Planning

The planner module performs basic preprocessing by:

- Cleaning whitespace
- Normalizing the query
- Determining whether retrieval is required

---

### Step 3 — Semantic Retrieval

The processed query is converted into an embedding using a Sentence Transformer model.

The embedding is compared against the FAISS vector index to retrieve the most semantically similar document chunks.

---

### Step 4 — Role-Based Authorization

Retrieved chunks are filtered according to the user's role.

Unauthorized documents are removed before they are passed to the language model.

This ensures confidential enterprise information remains protected.

---

### Step 5 — Context Construction

Authorized document chunks are combined into a structured context.

Relevant metadata including source file, sheet name, page number, and row information is preserved for citation purposes.

---

### Step 6 — Prompt Generation

A structured prompt is constructed containing:

- System instructions
- Retrieved enterprise context
- User question

The prompt instructs the language model to answer only from the provided documents and avoid fabricating information.

---

### Step 7 — Response Generation

The prompt is sent to the Groq-hosted Large Language Model.

The model synthesizes information from multiple retrieved documents into a single coherent response.

The assistant is instructed to:

- Generate professional responses
- Avoid hallucinations
- Summarize multiple records naturally
- Use tables when appropriate
- Explain financial concepts only when explicitly requested

---

### Step 8 — Source Attribution

The generated answer is returned together with the metadata of all supporting documents.

Users can inspect:

- Source file
- Sheet
- Page
- Row
- Access level

to verify the response.

---

### Step 9 — Feedback Loop

Users may optionally provide feedback indicating whether the generated response was helpful.

Feedback is stored in SQLite against the specific chunks that produced the answer, and is then used to re-rank retrieval for semantically similar future questions (see the **Feedback Loop** feature above). This makes the system improve as it is used, rather than only collecting data for offline analysis.

---

# Project Structure

```
Enterprise-Financial-AI-Assistant/

│
├── api/
│   ├── routes.py
│   ├── schemas.py
│
├── engine/
│   ├── planner.py
│   ├── retrieval.py
│   ├── generator.py
│   ├── database.py
│   ├── embedding.py
│   ├── feedback.py
│   ├── feedback_ranker.py
│   ├── rbac.py
│
├── frontend/
│   ├── streamlit_app.py
│   ├── api_client.py
│   ├── components.py
│   ├── styles.py
│
├── data/
│
├── vector_store/
│
├── requirements.txt
│
└── README.md
```

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLite
- FAISS
- Pydantic

---

## Artificial Intelligence

- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- Semantic Search
- Vector Embeddings
- Prompt Engineering
- Groq LLM

---

## Frontend

- Streamlit
- Custom CSS

---

# API Endpoints

## Health Check

```
GET /health
```

Returns backend status.

---

## Ask Question

```
POST /ask
```

Example Request

```json
{
    "question":"What was Apple's stock price?",
    "role":"Finance"
}
```

Example Response

```json
{
    "answer":"...",
    "sources":[
        {
            "source":"company_market_data.xlsx",
            "sheet":"Market Data",
            "row":5,
            "access":"Finance",
            "chunk_id":"a1b2c3d4"
        }
    ],
    "chunk_ids":["a1b2c3d4","e5f6g7h8"]
}
```

The `chunk_ids` identify the chunks used to build the answer. The client sends them back with feedback so ratings can be tied to specific retrieved chunks and fed into the retrieval loop.

---

## Submit Feedback

```
POST /feedback
```

Example Request

```json
{
    "question":"What is Apple's market capitalization?",
    "rating":5,
    "comment":"Helpful",
    "chunk_ids":["a1b2c3d4","e5f6g7h8"]
}
```

---

## Feedback Statistics

```
GET /feedback/stats
```

Returns an aggregate view of collected feedback.

Example Response

```json
{
    "total":42,
    "average_rating":4.1,
    "positive":30,
    "negative":8,
    "chunks_with_feedback":25
}
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<username>/enterprise-financial-ai-assistant.git
```

Move into the project directory.

```bash
cd financial-ai-assistant
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows

```bash
.venv\Scripts\activate
```

macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_api_key
LLM_MODEL=llama-3.3-70b-versatile
```

---

# Running the Backend

```bash
uvicorn app.main:app --reload
```

---

# Running the Frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

# Example Questions

- What was Apple's stock price in 2007?
- Compare Google's stock price across different years.
- What is EBITDA?
- Show Microsoft's market capitalization.
- Which company has the highest revenue?
- Explain stock price.

---

# Current Limitations

- The quality of generated responses depends on the relevance of retrieved document chunks.
- Retrieval is based on semantic similarity re-ranked with user feedback, but does not currently combine lexical (keyword) search.
- The feedback loop improves ranking of already-indexed chunks; it does not yet fine-tune the embedding model or add new documents automatically.
- The system is optimized for structured enterprise financial datasets.

---

# Future Enhancements

- Hybrid semantic and keyword retrieval
- Feedback-driven fine-tuning of the embedding model (the current loop re-ranks; it does not yet retrain)
- Automatic financial chart generation
- Multi-turn conversational memory
- Enterprise authentication (OAuth/SSO)
- Advanced analytics dashboard
- Explainable retrieval with similarity scores
- Support for additional enterprise document formats
- Integration with cloud storage and enterprise knowledge repositories

---

# License

This project is intended for educational, research, and demonstration purposes.