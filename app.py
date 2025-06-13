from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from guess_validator import validate_guess
from grid_generator import generate_grid

app = Flask(name)
CORS(app)

✅ Serve today's grid from the database (not file)

@app.route("/grid", methods=["GET"])
def get_grid():
toronto_today = datetime.now(ZoneInfo("America/Toronto")).date().isoformat()
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
else:  
    return jsonify({"error": "Grid for today not found"}), 404

✅ Validate a guess and return result + optional image

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

✅ Get list of queens

@app.route("/queens", methods=["GET"])
def list_queens():
conn = sqlite3.connect("dragdoku.db")
cur = conn.cursor()
cur.execute("SELECT DISTINCT queen_name FROM queens ORDER BY queen_name ASC")
names = [row[0] for row in cur.fetchall()]
conn.close()
return jsonify(names)

✅ Generate today's grid manually

@app.route("/generate", methods=["GET"])
def generate_today_grid():
result = generate_grid()
if result:
return jsonify({"status": "✅ Grid generated!"})
else:
return jsonify({"status": "❌ Failed to generate grid"}), 500

if name == "main":
app.run(debug=True)
