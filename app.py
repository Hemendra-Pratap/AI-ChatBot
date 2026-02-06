from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API key from environment variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Create model instance
model = genai.GenerativeModel("gemini-1.5-pro")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        prompt = data.get("message", "").strip()

        if not prompt:
            return jsonify({"error": "Empty message"}), 400

        response = model.generate_content(prompt)

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()

