from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import base64

app = Flask(__name__)
CORS(app)

# 🔑 Configure Gemini
genai.configure(api_key="AIzaSyDpP_u1enjbWlv7uVHLIwbNsL7k3Os7XRU")

# Use new model (gemini-1.5-flash or gemini-1.5-pro)
model = genai.GenerativeModel("gemini-1.5-flash")

# 🔹 TEXT ONLY
@app.route("/gemini-text", methods=["POST"])
def gemini_text():
    try:
        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return jsonify({"reply": "No question provided."})

        response = model.generate_content(message)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


# 🔹 IMAGE + TEXT
@app.route("/gemini-image", methods=["POST"])
def gemini_image():
    try:
        data = request.get_json()
        image_base64 = data.get("image")

        if not image_base64:
            return jsonify({"reply": "No image data received."})

        image_bytes = base64.b64decode(image_base64)

        response = model.generate_content([
            "Describe or answer the question in this image:",
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])

        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
