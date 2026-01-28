from flask import Blueprint, request, jsonify
from datetime import datetime
from bot import classify_message, bot_reply

chat_bp = Blueprint("chat", __name__)

messages = []
last_commitments = {}

@chat_bp.route("/chat/send", methods=["POST"])
def send():
    data = request.json
    user = data["user"]
    text = data["text"]

    msg_type = classify_message(text)

    msg = {
        "user": user,
        "text": text,
        "type": msg_type,
        "time": datetime.utcnow().isoformat()
    }
    messages.append(msg)

    if msg_type == "commitment":
        last_commitments[user] = {
            "message": text,
            "time": msg["time"]
        }

    reply = bot_reply(msg_type)
    if reply:
        messages.append({
            "user": "AI_Bot",
            "text": reply,
            "type": "ai",
            "time": datetime.utcnow().isoformat()
        })

    return jsonify(msg)

@chat_bp.route("/chat/messages")
def get_messages():
    return jsonify(messages)

@chat_bp.route("/chat/commitments")
def commitments():
    return jsonify(last_commitments)
