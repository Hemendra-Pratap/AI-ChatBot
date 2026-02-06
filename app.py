from flask import Flask, render_template, request, jsonify
from google import genai
import os
# Initialize Flask app
app = Flask(__name__)

# Initialize Google GenAI client

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt]
        )
        
        return jsonify({"response": response.text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()



