# initialize_databasestables.py
import pandas as pd
import sqlite3
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import GENERAL_NOTES_PDF, HTS_CSV_PATH, DB_PATH, CHROMA_PATH, COUNTRY_MAP

def init_sqlite_db():
    """Initialize SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.close()

def store_hts_csv():
    """Load HTS CSV into SQLite, enhancing fields."""
    try:
        df = pd.read_csv(HTS_CSV_PATH)
        if 'Chapter' in df.columns:
            df = df[df['Chapter'].isin([1, 2, 3, 4, 5])]
        if 'Country Code' in df.columns:
            df['Country_Name'] = df['Country Code'].map(COUNTRY_MAP).fillna(df['Country Code'])
        df.columns = [col.replace(" ", "_").replace("(", "").replace(")", "") for col in df.columns]
        conn = sqlite3.connect(DB_PATH)
        df.to_sql('hts_data', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Successfully created {DB_PATH} with HTS data.")
    except Exception as e:
        print(f"Error creating hts_data.db: {e}")

def ingest_general_notes():
    """Ingest and chunk General Notes PDF, store in Chroma."""
    try:
        loader = PyPDFLoader(GENERAL_NOTES_PDF)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
        print(f"Successfully created {CHROMA_PATH} vector store.")
    except Exception as e:
        print(f"Error creating chroma_db: {e}")

def verify_chroma():
    """Verify Chroma vector store content."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    count = vectorstore._collection.count()
    print(f"Chroma vector store contains {count} document chunks.")

def main():
    print("Initializing databases...")
    init_sqlite_db()
    store_hts_csv()
    ingest_general_notes()
    verify_chroma()
    print("Database initialization complete.")

if __name__ == "__main__":
    main()