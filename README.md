# Phishing URL Detection Website

This project is a Flask-based backend for detecting phishing URLs using a machine learning model. It provides API endpoints for checking URLs and retrieving the detection history.

## Features
- ML-based phishing detection
- URL history tracking
- Ready for frontend integration

## How to Run
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) Train and save a model as `phishing_model.pkl` (see below).
3. Start the backend:
   ```bash
   python app.py
   ```

## API Endpoints
- `POST /api/check_url` with JSON `{ "url": "http://example.com" }`
- `GET /api/history` to retrieve checked URLs and results

## Model Training
You need a trained ML model saved as `phishing_model.pkl`. You can use scikit-learn for this. If the file is missing, the backend will always return 'legit'.

## Deployment
You can deploy this app to platforms like Heroku, Render, or use Docker.

## GitHub Setup
1. Initialize the repo:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. Create a GitHub repo online and follow the instructions to push your code.
