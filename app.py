import os
import re
import joblib
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model + vectorizer
vectorizer = joblib.load(os.path.join(BASE_DIR, "vectorizer.pkl"))
model = joblib.load(os.path.join(BASE_DIR, "spam_stacking_model.pkl"))

def clean_text(text):
    text = re.sub('<[^>]*>', '', text)
    text = re.sub('[^a-zA-Z\s]', '', text)
    text = text.lower()
    text = re.sub('\s+', ' ', text).strip()
    return text

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    email_text = data.get("text", "")

    cleaned = clean_text(email_text)
    x = vectorizer.transform([cleaned])
    pred = model.predict(x)[0]
    proba = model.predict_proba(x)[0]

    return jsonify({
        "prediction": "SPAM" if pred == 1 else "HAM",
        "spam_confidence": float(proba[1]),
        "ham_confidence": float(proba[0])
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
