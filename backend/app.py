from flask import Flask, request, jsonify
from flask_cors import CORS
from chat import chat_bp
from alert_engine import generate_alerts
from leaderboard import compute_leaderboard

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_bp)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/alerts", methods=["POST"])
def alerts():
    data = request.json
    alerts = generate_alerts(data["user"], data["behavior"], data["task"])
    return jsonify(alerts)

@app.route("/leaderboard", methods=["POST"])
def leaderboard():
    leaderboard = compute_leaderboard(request.json)
    return jsonify(leaderboard)

if __name__ == "__main__":
    app.run(debug=True)
