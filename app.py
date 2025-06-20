from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from guess_validator import validate_guess
from grid_generator import generate_grid

app = Flask(__name__)
CORS(app)

PUZZLE_DIR = os.path.join(os.path.dirname(__file__), "puzzles")

def load_puzzle_from_file(date_str):
    path = os.path.join(PUZZLE_DIR, f"{date_str}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_puzzle_to_file(date_str, grid_data):
    os.makedirs(PUZZLE_DIR, exist_ok=True)
    path = os.path.join(PUZZLE_DIR, f"{date_str}.json")
    with open(path, "w") as f:
        json.dump(grid_data, f, indent=2)

@app.route("/grid", methods=["GET"])
def get_grid():
    today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
    
    # 1) Try load puzzle JSON from local file
    grid = load_puzzle_from_file(today)
    if grid:
        return jsonify(grid)
    
    # 2) If no local file, generate new grid (which also pushes to GitHub)
    grid = generate_grid()
    if grid:
        save_puzzle_to_file(today, grid)
        return jsonify(grid)
    
    return jsonify({"error": "Failed to generate grid"}), 500

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

@app.route("/queens", methods=["GET"])
def list_queens():
    import sqlite3
    conn = sqlite3.connect("dragdoku.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT queen_name FROM queens ORDER BY queen_name ASC")
    names = [row[0] for row in cur.fetchall()]
    conn.close()
    return jsonify(names)

@app.route("/generate", methods=["GET"])
def generate_today_grid():
    grid = generate_grid()
    if grid:
        today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
        save_puzzle_to_file(today, grid)
        return jsonify({"status": "✅ Grid generated!"})
    else:
        return jsonify({"status": "❌ Failed to generate grid"}), 500

if __name__ == "__main__":
    app.run(debug=True)
