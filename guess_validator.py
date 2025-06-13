import sqlite3
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import os
# Get today in Toronto timezone
toronto_today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()

# DB path (static)
DB_PATH = os.path.join(os.path.dirname(__file__), "dragdoku.db")

# Fetch today's grid SQL logic from the database
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("SELECT row_sql, col_sql FROM grids WHERE date = ?", (toronto_today,))
row = cur.fetchone()
conn.close()

if row:
    row_sql_list = json.loads(row[0])
    col_sql_list = json.loads(row[1])
else:
    row_sql_list = []
    col_sql_list = []

def validate_guess(row_idx, col_idx, queen_name):
    if row_idx >= len(row_sql_list) or col_idx >= len(col_sql_list):
        return False, "❌ Grid not loaded or invalid index.", None

    row_sql = row_sql_list[row_idx]
    col_sql = col_sql_list[col_idx]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    query = f"""
        SELECT image
        FROM queens
        WHERE lower(queen_name) = ?
        AND ({row_sql}) AND ({col_sql})
    """
    cur.execute(query, (queen_name.lower(),))
    match = cur.fetchone()
    conn.close()

    if match:
        return True, "✅ Correct!", match[0]
    else:
        return False, "❌ Not a valid match for this cell.", None
