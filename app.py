from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sqlite3
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from guess_validator import validate_guess
from grid_generator import generate_grid

app = Flask(__name__)
CORS(app)

# Supabase settings
SUPABASE_URL = "https://ubnphrvwjzucdawtbmws.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVibnBocnZ3anp1Y2Rhd3RibXdzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAyNzgxOTYsImV4cCI6MjA2NTg1NDE5Nn0.StVlYNhc95G7LPzeKzHprnTwY6R7DQ2sxJs8GdQryyA"

# ✅ Serve today's grid from local DB or Supabase or generate new
@app.route("/grid", methods=["GET"])
def get_grid():
    toronto_today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
    filename = f"grid_{toronto_today}.json"

    # 1. Try local database
    conn = sqlite3.connect("dragdoku.db")
    cur = conn.cursor()
    cur.execute("SELECT rows, cols, row_sql, col_sql, row_desc, col_desc, answers FROM grids WHERE date = ?", (toronto_today,))
    result = cur.fetchone()
    conn.close()

    if result:
        rows, cols, row_sql, col_sql, row_desc, col_desc, answers = map(json.loads, result)
        return jsonify({
            "rows": rows,
            "cols": cols,
            "row_sql": row_sql,
            "col_sql": col_sql,
            "row_desc": row_desc,
            "col_desc": col_desc,
            "answers": answers
        })

    # 2. Try Supabase
    res = requests.get(
        f"{SUPABASE_URL}/storage/v1/object/public/grids/{filename}",
        headers={"apikey": SUPABASE_KEY}
    )
    if res.status_code == 200:
        return jsonify(res.json())

    # 3. Fallback: generate and upload to Supabase
    grid_data = generate_grid()
    if grid_data:
        upload_grid_to_supabase(grid_data, filename)
        return jsonify(grid_data)
    else:
        return jsonify({"error": "Failed to generate grid"}), 500

def upload_grid_to_supabase(data, filename):
    url = f"{SUPABASE_URL}/storage/v1/object/grids/{filename}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    res = requests.put(url, headers=headers, data=json.dumps(data))
    print("📦 Uploaded to Supabase:", res.status_code)

# ✅ Validate a guess
@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    row = data.get("row")
    col = data.get("col")
    queen = data.get("queen")

    if row is None or col is None or not queen:
        return jsonify({"error": "Missing data"}), 400

    is_valid, message, image_url = validate_guess(row, col, queen)
    return jsonify({
        "valid": is_valid,
        "message": message,
        "queen": queen,
        "image": image_url
    })

# ✅ Get all queens
@app.route("/queens", methods=["GET"])
def list_queens():
    conn = sqlite3.connect("dragdoku.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT queen_name FROM queens ORDER BY queen_name ASC")
    names = [row[0] for row in cur.fetchall()]
    conn.close()
    return jsonify(names)

# ✅ Manually trigger grid generation
@app.route("/generate", methods=["GET"])
def generate_today_grid():
    result = generate_grid()
    if result:
        date = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
        filename = f"grid_{date}.json"
        upload_grid_to_supabase(result, filename)
        return jsonify({"status": "✅ Grid generated and uploaded!"})
    else:
        return jsonify({"status": "❌ Failed to generate grid"}), 500

if __name__ == "__main__":
    app.run(debug=True)
