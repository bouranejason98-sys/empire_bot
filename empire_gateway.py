from flask import Flask, request, jsonify, abort
from intelligence import route_message
from memory_engine import MemoryEngine
from learning import LearningEngine
from cloning_engine import resolve_clone

app = Flask(__name__)
memory = MemoryEngine()
learner = LearningEngine()

@app.route("/handle", methods=["POST"])
def handle():
    data = request.json
    if not data or "user" not in data or "message" not in data:
        abort(400, description="Missing 'user' or 'message' in request")

    user = data["user"]
    message = data["message"]
    clone_info = data.get("clone") or resolve_clone(user)

    try:
        result = route_message(user, message, clone_info)
        memory.remember(user, clone_info["id"], result["intent"], message, result["confidence"])
        improvement = learner.improve_response(user, clone_info["id"])
        if improvement:
            result["reply"] += "\n\n" + improvement
        memory.log_message(user, clone_info["id"], message, result["reply"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"reply":"⚠️ Error processing request","error":str(e)}),500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
