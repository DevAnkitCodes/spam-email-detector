import joblib
import re
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Path to files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "spam_stacking_model.pkl")

# Load model + vectorizer
try:
    vectorizer = joblib.load(VECTORIZER_PATH)
    model = joblib.load(MODEL_PATH)
    print("STATUS: Model & Vectorizer loaded successfully.")
except Exception as e:
    print(f"ERROR while loading model files: {e}")

# Clean text function
def clean_text(text):
    if not isinstance(text, str):
        text = ""

    text = re.sub("<[^>]*>", "", text)
    text = re.sub("[^a-zA-Z\\s]", "", text)
    text = text.lower()
    text = re.sub("\\s+", " ", text).strip()
    return text

# Home Page Route
@app.route("/")
def index():
    return render_template("index.html")

# Prediction Route
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    email_text = data.get("text", "")

    if not email_text:
        return jsonify({"error": "No text provided"}), 400

    cleaned = clean_text(email_text)
    X_test = vectorizer.transform([cleaned])

    prediction = model.predict(X_test)[0]
    proba = model.predict_proba(X_test)[0]

    result = {
        "prediction": "SPAM" if prediction == 1 else "HAM",
        "spam_confidence": float(proba[1]),
        "ham_confidence": float(proba[0]),
    }

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
