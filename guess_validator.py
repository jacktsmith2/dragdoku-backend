import sqlite3
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dragdoku.db")
PUZZLE_DIR = os.path.join(os.path.dirname(__file__), "puzzles")

def load_grid_criteria_from_file(date_str):
    path = os.path.join(PUZZLE_DIR, f"{date_str}.json")
    if not os.path.exists(path):
        return None, None
    with open(path, "r") as f:
        grid = json.load(f)
    row_sql = grid.get("row_sql")
    col_sql = grid.get("col_sql")
    return row_sql, col_sql

def validate_guess(row_idx, col_idx, queen_name):
    try:
        toronto_today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()

        row_sql_list, col_sql_list = load_grid_criteria_from_file(toronto_today)
        if not row_sql_list or not col_sql_list:
            return False, "❌ No grid found for today.", None

        if row_idx >= len(row_sql_list) or col_idx >= len(col_sql_list):
            return False, "❌ Invalid row or column index.", None

        row_sql = row_sql_list[row_idx]
        col_sql = col_sql_list[col_idx]

        # Run validation query on queens DB
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

    except Exception as e:
        print("❌ Validation error:", e)
        return False, "❌ Internal error.", None
