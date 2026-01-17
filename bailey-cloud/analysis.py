from flask import Flask, request, jsonify
from learning import log_interaction
from config import CLONE_ID

app = Flask(__name__)

def analyze_message(message: str) -> str:
    """
    Replace this with your existing analysis engine logic.
    """
    message = message.lower()

    if "house" in message or "home" in message:
        return "Here are some houses available in Nairobi. Would you like rentals or purchases?"
    elif "rent" in message:
        return "Great! Which area in Nairobi are you looking to rent in?"
    elif "buy" in message:
        return "Perfect. What’s your budget and preferred location?"
    else:
        return "I’m here to help with real estate in Kenya. What are you looking for?"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    user = data.get("user")
    message = data.get("message")

    reply = analyze_message(message)
    log_interaction(user, message, reply, CLONE_ID)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
