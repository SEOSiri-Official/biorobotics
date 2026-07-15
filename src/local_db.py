# src/local_db.py
import sqlite3
import os

# Define the database path inside your src folder
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_cache.db")

def init_db():
    """Initializes the local SQLite database and creates the cache table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS genomic_cache (
            gene_id TEXT PRIMARY KEY,
            sequence TEXT,
            concentration_proxy REAL
        )
    """)
    conn.commit()
    conn.close()

def get_cached_gene(gene_id: str):
    """Retrieves a cached gene record from the local database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sequence, concentration_proxy FROM genomic_cache WHERE gene_id = ?", 
        (gene_id.upper().strip(),)
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"sequence": row[0], "concentration_proxy": row[1]}
    return None

def cache_gene(gene_id: str, sequence: str, concentration_proxy: float):
    """Saves or updates a genomic record in the local cache database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO genomic_cache (gene_id, sequence, concentration_proxy)
        VALUES (?, ?, ?)
    """, (gene_id.upper().strip(), sequence, concentration_proxy))
    conn.commit()
    conn.close()