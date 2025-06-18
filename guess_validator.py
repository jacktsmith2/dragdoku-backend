import psycopg2
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import os

DATABASE_URL = os.environ["DATABASE_URL"]

def validate_guess(row_idx, col_idx, queen_name):
    try:
        toronto_today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()

        # Connect to database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Fetch today's grid
        cur.execute("SELECT row_sql, col_sql FROM grids WHERE date = %s", (toronto_today,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return False, "❌ No grid found for today.", None

        row_sql_list = json.loads(row[0])
        col_sql_list = json.loads(row[1])

        if row_idx >= len(row_sql_list) or col_idx >= len(col_sql_list):
            return False, "❌ Invalid row or column index.", None

        row_sql = row_sql_list[row_idx]
        col_sql = col_sql_list[col_idx]

        print(f"🧪 VALIDATING: {queen_name.lower()}")
        print(f"    Row SQL: {row_sql}")
        print(f"    Col SQL: {col_sql}")

        # Run validation
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        query = f"""
            SELECT image
            FROM queens
            WHERE lower(queen_name) = %s
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
