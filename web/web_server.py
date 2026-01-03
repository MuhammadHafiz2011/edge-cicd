from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()
    print("Web Server received data:", data, flush=True)
    return jsonify({"status": "stored"}), 200

@app.route("/", methods=["GET"])
def home():
    return "Web Server is running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

