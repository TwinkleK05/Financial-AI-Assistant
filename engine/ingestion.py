import pandas as pd
import pdfplumber
import uuid

from pathlib import Path
from typing import List


import logging
from config import RAW_DATA_DIR

from .database import Document

logger = logging.getLogger(__name__)

# ==================================================
# PDF INGESTION
# ==================================================

def read_pdf(file_path: Path) -> List[Document]:
    """
    Read one PDF and return one Document object per page.
    """

    logger.info(f"Reading PDF : {file_path.name}")

    documents = []

    try:

        with pdfplumber.open(file_path) as pdf:

            for page_number, page in enumerate(pdf.pages, start=1):

                text = page.extract_text()

                if not text:
                    continue

                documents.append(

                    Document(

                        id=str(uuid.uuid4()),

                        text=text,

                        source=file_path.name,

                        document_type="pdf",

                        access="public",

                        page=page_number

                    )

                )

    except Exception as error:

        logger.error(f"Error reading PDF {file_path.name}: {error}")

    return documents

# ==================================================
# EXCEL INGESTION
# ==================================================

def read_excel(file_path: Path) -> List[Document]:
    """
    Read an Excel workbook.
    Every row becomes one Document.
    """

    logger.info(f"Reading Excel : {file_path.name}")

    documents = []

    try:

        workbook = pd.read_excel(
            file_path,
            sheet_name=None
        )

        for sheet_name, dataframe in workbook.items():

            dataframe = dataframe.fillna("")

            for index, row in dataframe.iterrows():

                text = " | ".join(

                    f"{column}: {row[column]}"

                    for column in dataframe.columns

                )

                documents.append(

                    Document(

                        id=str(uuid.uuid4()),

                        text=text,

                        source=file_path.name,

                        document_type="excel",

                        access="finance",

                        sheet=sheet_name,

                        row=index + 1

                    )

                )

    except Exception as error:

        logger.error(f"Error reading Excel {file_path.name}: {error}")

    return documents

# ==================================================
# DOCUMENT INGESTION
# ==================================================

def process_uploaded_documents() -> List[Document]:
    """
    Read every supported document
    inside data/raw/
    """

    logger.info("Starting document ingestion...")

    documents = []

    for file in RAW_DATA_DIR.iterdir():

        suffix = file.suffix.lower()

        if suffix == ".pdf":

            documents.extend(

                read_pdf(file)

            )

        elif suffix in [".xlsx", ".xls"]:

            documents.extend(

                read_excel(file)

            )

    logger.info(f"Loaded {len(documents)} documents.")

    return documents

