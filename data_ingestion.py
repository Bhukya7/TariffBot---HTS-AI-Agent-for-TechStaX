# data_ingestion.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import GENERAL_NOTES_PDF, HTS_CSV_PATH, CHROMA_PATH
from database import store_hts_csv

def ingest_general_notes():
    """Ingest and chunk General Notes PDF, store in Chroma."""
    loader = PyPDFLoader(GENERAL_NOTES_PDF)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    return vectorstore

def ingest_hts_csv():
    """Ingest HTS CSV into SQLite."""
    store_hts_csv()