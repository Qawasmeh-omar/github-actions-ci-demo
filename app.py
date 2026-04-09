import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def home():
    return "Student Portal CI/CD Demo"


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/config")
def config_check():
    app_mode = os.getenv("APP_MODE")
    if not app_mode:
        return jsonify({"error": "APP_MODE is not set"}), 500
    return jsonify({"app_mode": app_mode})


@app.post("/grade")
def grade():
    data = request.get_json()

    if not data or "score" not in data:
        return jsonify({"error": "score is required"}), 400

    score = data["score"]

    if not isinstance(score, (int, float)):
        return jsonify({"error": "score must be numeric"}), 400

    if score < 0 or score > 100:
        return jsonify({"error": "score out of range"}), 400

    result = "pass" if score >= 50 else "fail"
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)