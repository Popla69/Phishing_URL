import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import re

# Example: Download a public phishing dataset (replace with your own for production)
# For demo, we'll use a small sample inline. In real use, load a CSV.
data = [
    {'url': 'http://secure-login.com', 'label': 1},
    {'url': 'https://google.com', 'label': 0},
    {'url': 'http://paypal-login.com', 'label': 1},
    {'url': 'https://github.com', 'label': 0},
    {'url': 'http://update-banking-info.com', 'label': 1},
    {'url': 'https://bankofamerica.com', 'label': 0},
    {'url': 'http://verify-account.com', 'label': 1},
    {'url': 'https://amazon.com', 'label': 0},
]
df = pd.DataFrame(data)

def extract_features(url):
    return {
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

# Load dataset from CSV file
# The CSV should have columns: URL, Label (Label should be 1 for phishing/malicious, 0 for safe)
df = pd.read_csv('phishing_site_urls.csv')
# Normalize column names if needed
df.columns = [col.strip().lower() for col in df.columns]
df.rename(columns={'url': 'url', 'label': 'label'}, inplace=True)
# Map string labels if present (e.g. 'bad'/'good' or 'phishing'/'legit')
if df['label'].dtype == object:
    df['label'] = df['label'].map(lambda x: 1 if str(x).lower() in ['bad','phishing','malicious','1'] else 0)
# Feature engineering
features = df['url'].apply(extract_features)
X = pd.DataFrame(list(features))
y = df['label']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print('Accuracy:', accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, 'phishing_model.pkl')
print('Model saved as phishing_model.pkl')
