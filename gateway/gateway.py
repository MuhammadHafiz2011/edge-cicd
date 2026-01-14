from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

WEB_SERVER_URL = "http://web-server:8000/ingest"

@app.route("/ingest", methods=["POST"])
def ingest():
    print("Gateway version CI/CD v2", flush=True)
    
    data = request.json
    print("Gateway received data:", data, flush=True)

    # Forward ke web server
    try:
        response = requests.post(WEB_SERVER_URL, json=data)
        print("Forwarded to web server:", response.status_code, flush=True)
    except Exception as e:
        print("Error forwarding to web server:", e, flush=True)

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
