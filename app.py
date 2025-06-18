from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import psycopg2
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from guess_validator import validate_guess
from grid_generator import generate_grid

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ["DATABASE_URL"]

# ✅ Serve today's grid from the PostgreSQL database
@app.route("/grid", methods=["GET"])
def get_grid():
    toronto_today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            SELECT rows, cols, row_sql, col_sql, row_desc, col_desc, answers
            FROM grids
            WHERE date = %s
        """, (toronto_today,))
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
        else:
            return jsonify({"error": "Grid for today not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# ✅ Validate a guess via external function
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

# ✅ Return a sorted list of queen names
@app.route("/queens", methods=["GET"])
def list_queens():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT queen_name FROM queens ORDER BY queen_name ASC")
        names = [row[0] for row in cur.fetchall()]
        conn.close()
        return jsonify(names)
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

# ✅ Manually trigger grid generation
@app.route("/generate", methods=["GET"])
def generate_today_grid():
    result = generate_grid()
    if result:
        return jsonify({"status": "✅ Grid generated!"})
    else:
        return jsonify({"status": "❌ Failed to generate grid"}), 500

if __name__ == "__main__":
    app.run(debug=True)
