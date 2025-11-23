import joblib
import re
import os 
from flask import Flask, request, jsonify
from flask_cors import CORS 

# ====================================================================
# 1. INITIAL SETUP
# ====================================================================

# CRITICAL FIX: The 'app' object MUST be created first.
app = Flask(__name__) 

# CORS allows your HTML file (frontend) to talk to this server (backend).
CORS(app) 

# Defines the base directory as the location of app.py.
# This ensures reliable file loading.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# ====================================================================
# 2. MODEL ARTIFACT LOADING (Change Path HERE if files are moved)
# ====================================================================

# Creates a reliable path to the .pkl files in the same directory.
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')
MODEL_PATH = os.path.join(BASE_DIR, 'spam_stacking_model.pkl')

try:
    # joblib.load() is used to read the saved Python objects.
    vectorizer = joblib.load(VECTORIZER_PATH)
    model = joblib.load(MODEL_PATH)
    print("STATUS: Model and Vectorizers loaded successfully!")
except Exception as e:
    print(f"ERROR: Failed to load model files. Check paths and permissions: {e}")
    # Consider raising an error or exiting if model loading fails
    # raise e 

# ====================================================================
# 3. TEXT CLEANING FUNCTION (MUST MATCH NOTEBOOK EXACTLY)
# ====================================================================

def clean_text(text):
    """
    Cleans the input text using the same logic (Cell 3) from the Jupyter Notebook.
    It is CRITICAL that this function is IDENTICAL to the one used for training.
    """
    if not isinstance(text, str):
        text = "" 
        
    # 1. Remove HTML tags
    text = re.sub('<[^>]*>', '', text)
    
    # 2. Remove special characters, punctuation, and numbers
    text = re.sub('[^a-zA-Z\s]', '', text)
    
    # 3. Convert to lowercase
    text = text.lower()
    
    # 4. Remove extra spaces
    text = re.sub('\s+', ' ', text).strip()
    
    return text

# ====================================================================
# 4. API ENDPOINT (The "Connection" Logic)
# ====================================================================

# This route listens for a POST request on http://127.0.0.1:5000/predict
@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data sent from the frontend (which contains the user's email text)
    data = request.get_json()
    email_text = data.get('text', '')
    
    if not email_text:
        return jsonify({'error': 'No text provided'}), 400
    
    # --- Prediction Logic ---
    
    # Step 1: Clean the text
    cleaned_text = clean_text(email_text)
    
    # Step 2: Vectorize the cleaned text using the loaded vectorizer
    X_test = vectorizer.transform([cleaned_text])
    
    # Step 3: Get the prediction (0=Ham, 1=Spam)
    prediction = model.predict(X_test)[0]
    
    # Step 4: Get the confidence (probability)
    # predict_proba returns [Prob_Ham, Prob_Spam]
    probability = model.predict_proba(X_test)[0]
    spam_prob = probability[1]
    
    # --- Format and Send Response ---
    
    result = {
        'prediction': 'SPAM' if prediction == 1 else 'HAM',
        'spam_confidence': float(spam_prob), 
        'ham_confidence': float(probability[0])
    }
    
    # Send the structured JSON result back to the frontend
    return jsonify(result)

# ====================================================================
# 5. RUN THE SERVER
# ====================================================================

if __name__ == '__main__':
    # Runs the server at http://127.0.0.1:5000/
    print("\nStarting Flask server...")
    print("STATUS: Server is running. Open index.html in your browser.")
    app.run(debug=True)