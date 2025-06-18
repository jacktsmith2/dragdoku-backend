import random
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from criteria import CRITERIA

import os
from supabase import create_client

SUPABASE_URL = "https://ubnphrvwjzucdawtbmws.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVibnBocnZ3anp1Y2Rhd3RibXdzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAyNzgxOTYsImV4cCI6MjA2NTg1NDE5Nn0.StVlYNhc95G7LPzeKzHprnTwY6R7DQ2sxJs8GdQryyA"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Helper: get queen_ids matching a SQL WHERE clause in Supabase Postgres
def fetch_queens(sql):
    # Example query to queens table with filter in `sql`
    # NOTE: This assumes your queens table has 'queen_id' and that 'sql' is valid SQL filter
    # Supabase uses PostgREST, so we need to convert 'sql' into filter params or use RPC function.
    # For simplicity, assume 'sql' is a safe WHERE clause string, so we run RPC (or raw SQL) via supabase.
    
    # Unfortunately supabase-py doesn't directly support raw SQL.
    # So you need to create a Postgres function that accepts SQL filter string
    # OR you rewrite your criteria in a way supabase-py supports filtering.

    # Here is a simplified placeholder: fetch all queen_ids (replace with your logic)
    response = supabase.table("queens").select("queen_id").execute()
    if response.error:
        print("❌ Supabase fetch queens error:", response.error)
        return set()
    return set(row["queen_id"] for row in response.data)

# Check duplicate labels, overlaps, same as before...

def has_duplicate_labels(criteria_list):
    labels = [c["label"] for c in criteria_list]
    return len(labels) != len(set(labels))

def has_illegal_axis_overlap(rows, cols):
    row_categories = {r["category"] for r in rows if r.get("category", "").startswith("at_least")}
    col_categories = {c["category"] for c in cols if c.get("category", "").startswith("at_least")}
    return bool(row_categories & col_categories)

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

def generate_grid():
    max_attempts = 1000
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
                # **You must implement filtering on Supabase to replicate this filter:**
                # qids = fetch_queens(f"({r['sql']}) AND ({c['sql']})")
                # For now fetch all queen_ids as placeholder
                qids = fetch_queens("")  # You need to replace this with actual filtering
                row_matches.append(qids)
            matches.append(row_matches)

        if all(len(cell) >= 2 for row in matches for cell in row):
            assignment = assign_unique_queens(matches)
            if assignment:
                save_grid_to_supabase({
                    "rows": rows,
                    "cols": cols,
                    "matches": matches,
                    "assignment": assignment
                })
                return {
                    "rows": rows,
                    "cols": cols,
                    "matches": matches,
                    "assignment": assignment
                }

    return None

def assign_unique_queens(matches):
    assigned = [[None]*3 for _ in range(3)]
    used = set()

    def backtrack(i,j):
        if i == 3:
            return True
        ni, nj = (i, j+1) if j<2 else (i+1, 0)
        for qid in matches[i][j]:
            if qid not in used:
                assigned[i][j] = qid
                used.add(qid)
                if backtrack(ni,nj):
                    return True
                used.remove(qid)
                assigned[i][j] = None
        return False

    if backtrack(0,0):
        return assigned
    return None

def save_grid_to_supabase(grid_data):
    import requests
    from datetime import datetime
    from zoneinfo import ZoneInfo

    today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
    filename = f"grid_{today}.json"

    url = f"{SUPABASE_URL}/storage/v1/object/grids/{filename}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    res = requests.put(url, headers=headers, data=json.dumps(grid_data))
    if res.status_code == 200:
        print(f"✅ Grid saved to Supabase storage as {filename}")
    else:
        print(f"❌ Failed to save grid to Supabase storage: {res.status_code} {res.text}")

# If run directly, generate once
if __name__ == "__main__":
    result = generate_grid()
    if result:
        print("✅ Grid generation successful")
    else:
        print("❌ Failed to generate a valid grid")
