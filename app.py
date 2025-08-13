from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

# In-memory URL history (for demo; can be replaced by DB)
url_history = []

# Load ML model (placeholder, replace with actual model after training)
MODEL_PATH = 'phishing_model.pkl'
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None  # Placeholder

# Feature extraction (simple; replace with real feature engineering)
def extract_features(url):
    features = {
        'url_length': len(url),
        'has_https': int('https' in url),
        'count_dots': url.count('.'),
        'count_slash': url.count('/'),
        'count_at': url.count('@'),
        'count_hyphen': url.count('-'),
        'count_question': url.count('?'),
        'count_equal': url.count('='),
        'count_percent': url.count('%'),
        'count_digits': sum(c.isdigit() for c in url)
    }
    return pd.DataFrame([features])

@app.route('/api/check_url', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    # Extract features
    features = extract_features(url)
    # Predict
    if model:
        result = model.predict(features)[0]
        proba = model.predict_proba(features)[0,1]
    else:
        result = 0  # Assume safe if no model
        proba = 0.0
    # Save to history
    url_history.append({
        'url': url,
        'result': 'phishing' if result else 'legit',
        'score': float(proba),
        'timestamp': datetime.now().isoformat()
    })
    return jsonify({'url': url, 'result': 'phishing' if result else 'legit', 'score': float(proba)})

@app.route('/api/history', methods=['GET'])
def get_history():
    return jsonify(url_history)

from flask import send_from_directory

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
