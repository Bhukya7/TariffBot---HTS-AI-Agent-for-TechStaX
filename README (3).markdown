# TariffBot - HTS AI Agent for TechStaX

## Overview
TariffBot is a Python-based AI agent designed for trade compliance, capable of answering trade-related questions, calculating customs duties, and retrieving Harmonized Tariff Schedule (HTS) codes. Built for the TechStaX challenge, it leverages a Chroma vector store for retrieval-augmented generation (RAG), SQLite for HTS data storage, and the BART model for concise responses.

## Features
- **RAG Queries**: Answers trade questions (e.g., "What is the United States-Israel Free Trade Agreement?") using a Chroma vector store with 3591 chunks from `General Notes.pdf`.
- **Tariff Calculations**: Computes duties based on HTS code, cost, weight, and quantity (e.g., "HTS code 0101.30.00.00, cost $10000, 500kg, 24 units").
- **Description Lookups**: Retrieves HTS codes by product description (e.g., "What's the HTS code for donkeys?") using SQLite.
- **Modular Design**: Integrates langchain, pandas, SQLite, and transformers for robust performance.

## Architecture
TariffBot processes queries through three pipelines: RAG, tariff calculation, and description lookup. Below is an ASCII diagram of the workflow:

```
+-------------------+
|    User Query     |
+-------------------+
         |
         v
+-------------------+
|   main.py         |
| (Query Parser)    |
+-------------------+
         |
         v
+-------------------+
|   handle_query()  |
| (Route Query)     |
+-------------------+
    |        |        |
    v        v        v
+---------+ +---------+ +---------+
| RAG      | | Tariff   | | Desc.    |
| (rag_tool| | (tariff_ | | (database|
|.py)     | | calc.py) | |.py)     |
+---------+ +---------+ +---------+
    |            |            |
    v            v            v
+---------+ +---------+ +---------+
| Chroma   | | SQLite   | | SQLite   |
| (General | | (hts_    | | (hts_    |
| Notes)   | | data.db) | | data.db) |
+---------+ +---------+ +---------+
    |
    v
+---------+
| BART     |
| (Summar- |
| ization) |
+---------+
```

- **RAG Pipeline**: Queries are vectorized using `sentence-transformers/all-MiniLM-L6-v2`, matched against Chroma, and summarized by BART.
- **Tariff Pipeline**: Parses HTS code, cost, weight, and quantity, queries SQLite for duty rates, and computes duties.
- **Description Pipeline**: Uses SQLite LIKE queries for case-insensitive description matching.

## Setup
### Prerequisites
- Python 3.10 (avoid 3.13 due to compatibility issues)
- Git
- Virtual environment (`venv`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/[YourUsername]/HTSAgent-Task-[YourName].git
   cd HTSAgent-Task-[YourName]
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/macOS
   ```

3. Install dependencies:
   ```bash
   pip install langchain-huggingface langchain-chroma langchain-community pandas pypdf sentence-transformers chromadb langchain transformers
   ```

4. Prepare data:
   - Place `hts_2024_revision_9_csv.csv` in `data/` (35,808 rows, provided or generated).
   - Place `General Notes.pdf` in `data/` (source for RAG).
   - Run ingestion scripts:
     ```bash
     python -c "from database import store_hts_csv; store_hts_csv()"
     python -c "from data_ingestion import ingest_general_notes; ingest_general_notes()"
     ```

### File Structure
```
HTSAgent/
├── data/
│   ├── hts_2024_revision_9_csv.csv
│   ├── General Notes.pdf
│   └── hts_data.db
├── append_donkeys.py
├── config.py
├── database.py
├── data_ingestion.py
├── main.py
├── rag_tool.py
├── tariff_calculator.py
├── test_db.py
├── requirements.txt
├── README.md
└── docs/
    └── architecture.png (optional)
```

## Usage
1. Run the bot:
   ```bash
   python main.py
   ```
   Output: `Welcome to TariffBot! Type 'exit' to quit.`

2. Example Queries:
   - **RAG Query**:
     ```
     Enter your query: What is the United States-Israel Free Trade Agreement?
     ```
     Output:
     ```
     The United States-Israel Free Trade Agreement, signed on April 22, 1985, grants preferential tariff treatment to eligible Israeli products in the U.S. It is implemented under the United States-Israel Free Trade Area Implementation Act of 1985.
     Sources: ['data\General Notes.pdf']
     ```

   - **Tariff Query**:
     ```
     Enter your query: HTS code 0101.30.00.00, cost $10000, 500kg, 24 units
     ```
     Output:
     ```
     HTS Code: 0101.30.00.00
     CIF Value: $10000.00
     Duty Rate: 0.00%
     Duty Amount: $0.00
     Total Weight: 12000 kg
     ```

   - **Description Query**:
     ```
     Enter your query: What's the HTS code for donkeys?
     ```
     Output:
     ```
     HTS Code for donkeys: 0101.30.00.00
     Description: Donkeys
     ```

3. Exit:
   ```
   Enter your query: exit
   ```

## Demo Video
Watch the demo video showcasing TariffBot’s features: [Google Drive Link](#) (placeholder, update after upload).

## Troubleshooting
- **Empty Database**:
  - Verify `hts_2024_revision_9_csv.csv` contains data:
    ```bash
    python -c "import pandas as pd; print(pd.read_csv('data/hts_2024_revision_9_csv.csv').shape)"
    ```
  - Re-ingest:
    ```bash
    python -c "from database import store_hts_csv; store_hts_csv()"
    ```

- **ImportError**:
  - Ensure `query_by_hts_code` is in `database.py`.
  - Check `tariff_calculator.py` imports.

- **RAG Issues**:
  - Revert to `distilgpt2`:
    ```python
    # config.py
    LLM_MODEL = "distilgpt2"
    ```
    ```python
    # rag_tool.py
    task = "text-generation"
    ```

- **Python 3.13**:
  - Downgrade to 3.10:
    ```bash
    python -m venv venv310
    .\venv310\Scripts\activate
    pip install -r requirements.txt
    ```

## License
MIT License. See [LICENSE](LICENSE) for details.

## Contact
For questions, contact [Your Name] at [Your Email].