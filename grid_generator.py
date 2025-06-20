import random
import json
import os
import requests
import base64
from datetime import datetime
from zoneinfo import ZoneInfo
from criteria import CRITERIA

# GitHub config
GITHUB_OWNER = "jacktsmith2"
GITHUB_REPO = "dragdoku-backend"
GITHUB_BRANCH = "main"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") 

def fetch_queens(sql):
    # Your existing queen fetch logic here
    return set()

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

def push_puzzle_to_github(grid_data, date):
    path = f"puzzles/{date}.json"
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    r = requests.get(url, headers=headers)
    sha = r.json().get("sha") if r.status_code == 200 else None

    data = {
        "message": f"Add puzzle for {date}",
        "content": base64.b64encode(json.dumps(grid_data, indent=2).encode()).decode(),
        "branch": GITHUB_BRANCH
    }
    if sha:
        data["sha"] = sha

    r = requests.put(url, headers=headers, json=data)
    if r.status_code in [200, 201]:
        print("✅ Puzzle pushed to GitHub")
    else:
        print(f"❌ GitHub push failed: {r.text}")

def fetch_grid_from_github(date):
    path = f"puzzles/{date}.json"
    url = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{path}"
    r = requests.get(url)
    if r.status_code == 200:
        print("✅ Puzzle loaded from GitHub")
        return r.json()
    print("⚠ No puzzle found on GitHub")
    return None

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
                qids = fetch_queens(f"({r['sql']}) AND ({c['sql']})")
                row_matches.append(qids)
            matches.append(row_matches)

        if all(len(cell) >= 2 for row in matches for cell in row):
            assignment = assign_unique_queens(matches)
            if assignment:
                today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
                grid_data = {
                    "rows": [r["label"] for r in rows],
                    "cols": [c["label"] for c in cols],
                    "row_sql": [r["sql"] for r in rows],       # <-- Add this
                    "col_sql": [c["sql"] for c in cols],       # <-- Add this
                    "row_desc": [r["description"] for r in rows], # Optional but useful
                    "col_desc": [c["description"] for c in cols], # Optional but useful
                    "answers": assignment
                }
                push_puzzle_to_github(grid_data, today)
                return grid_data
    print("❌ Failed to generate valid grid")
    return None

def load_or_generate_grid():
    today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
    grid = fetch_grid_from_github(today)
    if grid:
        return grid
    return generate_grid()

if __name__ == "__main__":
    grid = load_or_generate_grid()
    if grid:
        print(json.dumps(grid, indent=2))
    else:
        print("❌ No grid available")
