# Updated grid generator with category and label protection (Toronto timezone)

import sqlite3
import random
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from criteria import CRITERIA

conn = sqlite3.connect("dragdoku.db")
cur = conn.cursor()

# Helper: get queen_ids matching a SQL WHERE clause
def fetch_queens(sql):
    cur.execute(f"SELECT DISTINCT queen_id FROM queens WHERE {sql}")
    return set(row[0] for row in cur.fetchall())

# Check for duplicate labels
def has_duplicate_labels(criteria_list):
    labels = [c["label"] for c in criteria_list]
    return len(labels) != len(set(labels))

# Check for duplicate categories
def has_duplicate_categories(criteria_list):
    categories = [c.get("category") for c in criteria_list if "category" in c]
    return len(categories) != len(set(categories))

# Step 1: Try to generate a grid with 3x3 criteria combinations
def generate_grid():
    max_attempts = 500
    for _ in range(max_attempts):
        rows = random.sample(CRITERIA, 3)
        cols = random.sample(CRITERIA, 3)

        combined = rows + cols
        if has_duplicate_labels(combined) or has_duplicate_categories(combined):
            continue

        matches = []  # 3x3 grid of sets of queen_ids
        for r in rows:
            row_matches = []
            for c in cols:
                qids = fetch_queens(f"({r['sql']}) AND ({c['sql']})")
                row_matches.append(qids)
            matches.append(row_matches)

        if all(len(cell) >= 2 for row in matches for cell in row):
            assignment = assign_unique_queens(matches)
            if assignment:
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

# Step 3: Save result to a date-named file using Toronto time
result = generate_grid()
if result:
    toronto_today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
    filename = f"grid_{toronto_today}.json"

    output = {
        "rows": [r["label"] for r in result["rows"]],
        "cols": [c["label"] for c in result["cols"]],
        "row_sql": [r["sql"] for r in result["rows"]],
        "col_sql": [c["sql"] for c in result["cols"]],
        "row_desc": [r["description"] for r in result["rows"]],
        "col_desc": [c["description"] for c in result["cols"]],
        "answers": result["assignment"]
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Grid generated and saved to {filename}")
else:
    print("❌ Failed to generate a valid grid after many attempts.")
