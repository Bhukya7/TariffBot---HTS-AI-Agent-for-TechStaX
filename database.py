# database.py
import sqlite3
import pandas as pd
from config import HTS_CSV_PATH, DB_PATH

def store_hts_csv():
    """Store HTS CSV data in SQLite database."""
    df = pd.read_csv(HTS_CSV_PATH)
    df = df.rename(columns=lambda x: x.strip())
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('hts_data', conn, if_exists='replace', index=False)
    conn.close()

def query_by_description(description):
    """Query HTS data by product description."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT [HTS Number], Description FROM hts_data WHERE Description LIKE ?"
    df = pd.read_sql_query(query, conn, params=[f'%{description}%'])
    conn.close()
    return df

def query_by_hts_code(hts_code):
    """Query HTS data by HTS code."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT [HTS Number], Description, [General Rate of Duty], [Special Rate of Duty] FROM hts_data WHERE [HTS Number] = ?"
    df = pd.read_sql_query(query, conn, params=[hts_code])
    conn.close()
    return df