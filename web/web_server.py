from flask import Flask, request, jsonify

app = Flask(__name__)

latest_data = {}

@app.route("/")
def index():
    return "Web Server OK"

@app.route("/ingest", methods=["POST"])
def ingest():
    global latest_data
    latest_data = request.json
    print(f"Web Server received data: {latest_data}")
    return jsonify({"status": "received"}), 200

@app.route("/data/latest", methods=["GET"])
def get_latest():
    if not latest_data:
        return jsonify({"message": "No data yet"}), 200
    return jsonify(latest_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
