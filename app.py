from flask import Flask, jsonify
from config import HOME_MESSAGE

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": HOME_MESSAGE,
        "status": "success"
    })


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )