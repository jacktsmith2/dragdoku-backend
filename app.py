from flask import Flask, request, jsonify
import json
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

from guess_validator import validate_guess

app = Flask(__name__)

# Serve today's grid based on Toronto time
@app.route("/grid", methods=["GET"])
def get_grid():
    toronto_now = datetime.now(ZoneInfo("America/Toronto"))
    today = toronto_now.date().isoformat()
    filename = f"grid_{today}.json"

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Today's grid not found."}), 404

# Validate a guess
@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    row = data.get("row")
    col = data.get("col")
    queen = data.get("queen")

    if row is None or col is None or not queen:
        return jsonify({"error": "Missing data"}), 400

    is_valid, message, _ = validate_guess(row, col, queen)
    return jsonify({
        "valid": is_valid,
        "message": message,
        "queen": queen
    })

# Get list of queens
@app.route("/queens", methods=["GET"])
def list_queens():
    conn = sqlite3.connect("dragdoku.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT queen_name FROM queens ORDER BY queen_name ASC")
    names = [row[0] for row in cur.fetchall()]
    conn.close()
    return jsonify(names)
    
if __name__ == "__main__":
    app.run(debug=True)
