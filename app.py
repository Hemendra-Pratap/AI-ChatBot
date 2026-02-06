from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# Create Gemini client using environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        prompt = data.get("message", "").strip()

        if not prompt:
            return jsonify({"error": "Empty message"}), 400

        response = client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=prompt
        )

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()


@app.route("/models")
def list_models():
    try:
        models = client.models.list()
        return jsonify([m.name for m in models])
    except Exception as e:
        return jsonify({"error": str(e)}), 500




