# app.py
from flask import Flask, request, jsonify
from task_breakdown_model import TaskBreakdownModel
app = Flask(__name__)
model = TaskBreakdownModel()

@app.route("/")
def home():
    return "🧠 Neurodiversity Task Breakdown API is running!"

@app.route("/breakdown", methods=["POST"])
def breakdown():
    data = request.get_json()
    task = data.get("task", "")
    if not task:
        return jsonify({"error": "No task provided"}), 400
    steps = model.breakdown_task(task)
    return jsonify({"original_task": task, "breakdown": steps})

if __name__ == "__main__":
    app.run(debug=True)
