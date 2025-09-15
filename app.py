from flask import Flask, send_from_directory, jsonify, request
from datetime import datetime

app = Flask(__name__, static_folder="static")

# Mock data
ongoing_productions = [
    {"id": 1, "name": "Ürün A-123", "start": "10:30", "target": 500, "current": 325, "status": "ongoing"},
    {"id": 2, "name": "Ürün B-456", "start": "09:15", "target": 300, "current": 120, "status": "ongoing"},
]

history_productions = [
    {"id": 3, "name": "Ürün C-789", "start": "10:00", "end": "14:30", "target": 400, "produced": 400, "status": "completed"},
    {"id": 4, "name": "Ürün D-012", "start": "08:00", "end": "12:45", "target": 250, "produced": 250, "status": "completed"},
    {"id": 5, "name": "Ürün E-345", "start": "13:00", "end": "13:45", "target": 200, "produced": 45, "status": "canceled"},
]

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/ongoing")
def get_ongoing():
    return jsonify(ongoing_productions)

@app.route("/api/history")
def get_history():
    return jsonify(history_productions)

@app.route("/api/production", methods=["POST"])
def add_production():
    data = request.json
    new_id = max([p["id"] for p in ongoing_productions + history_productions], default=0) + 1
    new_production = {
        "id": new_id,
        "name": data.get("name", f"Ürün-{new_id}"),
        "start": datetime.now().strftime("%H:%M"),
        "target": data.get("target", 100),
        "current": 0,
        "status": "ongoing"
    }
    ongoing_productions.append(new_production)
    return jsonify({"message": "Yeni üretim eklendi", "production": new_production}), 201

if __name__ == "__main__":
    app.run(debug=True)
