import sqlite3
import json
from datetime import datetime
from zoneinfo import ZoneInfo

# Load today's grid based on Toronto time
toronto_today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
with open(f"grid_{toronto_today}.json", "r", encoding="utf-8") as f:
    grid = json.load(f)

def validate_guess(row_idx, col_idx, queen_name):
    row_sql = grid["row_sql"][row_idx]
    col_sql = grid["col_sql"][col_idx]

    conn = sqlite3.connect("dragdoku.db")
    cur = conn.cursor()

    # First, check if this queen is a valid match for the given cell
    query = f"""
        SELECT image
        FROM queens
        WHERE lower(queen_name) = ?
          AND ({row_sql}) AND ({col_sql})
    """
    cur.execute(query, (queen_name.lower(),))
    match = cur.fetchone()

    if match:
        image_url = match[0]
        conn.close()
        return True, "✅ Correct!", image_url
    else:
        # Try to still get the image even if the guess is incorrect
        cur.execute("SELECT image FROM queens WHERE lower(queen_name) = ?", (queen_name.lower(),))
        fallback = cur.fetchone()
        conn.close()
        return False, "❌ Not a valid match for this cell.", fallback[0] if fallback else None
