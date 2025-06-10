# test_db.py
import sqlite3
import pandas as pd

conn = sqlite3.connect('hts_data.db')
df = pd.read_sql_query("SELECT [HTS Number], Description FROM hts_data WHERE Description LIKE '%donkey%'", conn)
print(df)
conn.close()