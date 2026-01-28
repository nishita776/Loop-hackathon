from flask import Flask
from flask_cors import CORS
from chat import chat_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_bp)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
