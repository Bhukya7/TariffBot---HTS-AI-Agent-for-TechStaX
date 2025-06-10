# config.py
import os

GENERAL_NOTES_PDF = os.path.join("data", "General Notes.pdf")
HTS_CSV_PATH = os.path.join("data", "hts_2024_revision_9_csv.csv")
DB_PATH = "hts_data.db"
CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "facebook/bart-base"
COUNTRY_MAP = {
    "AU": "Australia",
    "US": "United States",
    "IL": "Israel",
    "CA": "Canada",
    "MX": "Mexico"
}