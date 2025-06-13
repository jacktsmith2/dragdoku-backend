from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route("/run-grid", methods=["POST"])
def run_grid():
    try:
        subprocess.run(["python3", "grid_generator.py"], check=True)
        return jsonify({"status": "✅ Grid generated."})
    except subprocess.CalledProcessError:
        return jsonify({"status": "❌ Grid generation failed."}), 500

if __name__ == "__main__":
    app.run(debug=True)
