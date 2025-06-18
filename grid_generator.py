import os
import random
import json
import psycopg2
from datetime import datetime
from zoneinfo import ZoneInfo
from criteria import CRITERIA

DATABASE_URL = os.environ["DATABASE_URL"]

# Helper: get queen_ids matching a SQL WHERE clause
def fetch_queens(sql, conn):
    try:
        cur = conn.cursor()
        print(f"Running SQL: SELECT DISTINCT queen_id FROM queens WHERE {sql}")
        cur.execute(f"SELECT DISTINCT queen_id FROM queens WHERE {sql}")
        rows = cur.fetchall()
        return [r[0] for r in rows]
    except Exception as e:
        print(f"SQL error: {e}")
        raise

# Check for duplicate labels
def has_duplicate_labels(criteria_list):
    labels = [c["label"] for c in criteria_list]
    return len(labels) != len(set(labels))

# Check for forbidden 'at_least' category overlaps
def has_illegal_axis_overlap(rows, cols):
    row_categories = {r["category"] for r in rows if r.get("category", "").startswith("at_least")}
    col_categories = {c["category"] for c in cols if c.get("category", "").startswith("at_least")}
    return bool(row_categories & col_categories)

# Detect conflicting numeric ranges like "1 Maxi Win" x "1+ Maxi Win"
def range_overlap(a, b):
    return not (a["max"] < b["min"] or b["max"] < a["min"])

def has_conflicting_numeric_overlap(rows, cols):
    for r in rows:
        for c in cols:
            if r.get("category") == c.get("category"):
                if "min" in r and "max" in r and "min" in c and "max" in c:
                    if range_overlap(r, c):
                        return True
    return False

# Step 1: Try to generate a grid with 3x3 criteria combinations
def generate_grid():
    max_attempts = 1000
    with psycopg2.connect(DATABASE_URL) as conn:
        for _ in range(max_attempts):
            rows = random.sample(CRITERIA, 3)
            cols = random.sample(CRITERIA, 3)
            combined = rows + cols

            if has_duplicate_labels(combined):
                continue
            if has_illegal_axis_overlap(rows, cols):
                continue
            if has_conflicting_numeric_overlap(rows, cols):
                continue

            matches = []
            for r in rows:
                row_matches = []
                for c in cols:
                    qids = fetch_queens(f"({r['sql']}) AND ({c['sql']})", conn)
                    row_matches.append(qids)
                matches.append(row_matches)

            if all(len(cell) >= 2 for row in matches for cell in row):
                assignment = assign_unique_queens(matches)
                if assignment:
                    save_grid_to_db(rows, cols, assignment)
                    return {
                        "rows": rows,
                        "cols": cols,
                        "matches": matches,
                        "assignment": assignment
                    }
    return None

# Step 2: Assign one unique queen_id to each of the 9 cells
def assign_unique_queens(matches):
    assigned = [[None for _ in range(3)] for _ in range(3)]
    used = set()

    def backtrack(i, j):
        if i == 3:
            return True
        ni, nj = (i, j + 1) if j < 2 else (i + 1, 0)
        for qid in matches[i][j]:
            if qid not in used:
                assigned[i][j] = qid
                used.add(qid)
                if backtrack(ni, nj):
                    return True
                used.remove(qid)
                assigned[i][j] = None
        return False

    if backtrack(0, 0):
        return assigned
    return None

# Step 3: Save the grid into the PostgreSQL database
def save_grid_to_db(rows, cols, assignment):
    print("🧪 save_grid_to_db called")
    today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()

    with psycopg2.connect(DATABASE_URL) as conn:
        cur = conn.cursor()

        cur.execute("DELETE FROM grids WHERE date = %s", (today,))
        print("🧽 Old grid deleted (if existed)")

        cur.execute("""
            INSERT INTO grids (date, rows, cols, row_sql, col_sql, row_desc, col_desc, answers)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            today,
            json.dumps([r["label"] for r in rows]),
            json.dumps([c["label"] for c in cols]),
            json.dumps([r["sql"] for r in rows]),
            json.dumps([c["sql"] for c in cols]),
            json.dumps([r["description"] for r in rows]),
            json.dumps([c["description"] for c in cols]),
            json.dumps(assignment)
        ))

        conn.commit()
        print("✅ Grid for", today, "committed to PostgreSQL")
