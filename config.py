"""
config.py

Central configuration file for the Financial AI Assistant.

This file stores:
1. Project folder paths
2. Gemini configuration
3. Embedding configuration
4. Chunking configuration
5. Retrieval configuration
6. RBAC configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

# Gemini API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL = "llama-3.3-70b-versatile"

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

FEEDBACK_FILE = BASE_DIR / "feedback.json"

DATABASE_PATH = BASE_DIR / "financial_data.db"

FAISS_INDEX_PATH = PROCESSED_DATA_DIR / "faiss.index"

CHUNKS_FILE = PROCESSED_DATA_DIR / "chunks.json"

METADATA_FILE = PROCESSED_DATA_DIR / "metadata.json"

SUMMARIES_FILE = PROCESSED_DATA_DIR / "summaries.json"

VECTOR_MAPPING_PATH = PROCESSED_DATA_DIR / "vector_mapping.json"

# --------------------------------------------------
# Embedding Configuration
# --------------------------------------------------

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --------------------------------------------------
# Chunking Configuration
# --------------------------------------------------

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# --------------------------------------------------
# Retrieval Configuration
# --------------------------------------------------

TOP_K_RESULTS = 5

# --------------------------------------------------
# Supported File Types
# --------------------------------------------------

SUPPORTED_FILE_TYPES = [
    ".pdf",
    ".xlsx",
    ".xls"
]

# --------------------------------------------------
# Role Based Access Control (RBAC)
# --------------------------------------------------

ROLE_PERMISSIONS = {

    "CEO": [
        "public",
        "finance",
        "executive"
    ],

    "Finance": [
        "public",
        "finance"
    ],

    "CTO": [
        "public"
    ],

    "Intern": [
        "public"
    ]
}