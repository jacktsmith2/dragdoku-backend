import sqlite3
import json
import datetime

# Use today's grid
today = datetime.date.today().isoformat()
with open(f"grid_{today}.json", "r", encoding="utf-8") as f:
    grid = json.load(f)

def validate_guess(row_idx, col_idx, queen_name):
    row_sql = grid["row_sql"][row_idx]
    col_sql = grid["col_sql"][col_idx]

    conn = sqlite3.connect("dragdoku.db")
    cur = conn.cursor()

    query = f"""
        SELECT queen_id
        FROM queens
        WHERE lower(queen_name) = ?
        AND ({row_sql}) AND ({col_sql})
    """
    cur.execute(query, (queen_name.lower(),))
    match = cur.fetchone()
    conn.close()

    if match:
        return True, "✅ Correct!", queen_name
    else:
        return False, "❌ Not a valid match for this cell.", None