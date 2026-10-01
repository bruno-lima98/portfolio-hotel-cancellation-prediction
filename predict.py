"""
predict.py

Flask web service that serves the hotel booking cancellation model.
Exposes a single POST endpoint, /predict, that receives one reservation's
data as JSON and returns the predicted cancellation probability plus the
binary decision at the cost-optimized threshold (Section 11 of the workbook).

Run locally for testing:
    Windows:      waitress-serve --listen=0.0.0.0:9696 predict:app
    Linux/Docker: gunicorn --bind=0.0.0.0:9696 predict:app
"""

from flask import Flask, request, jsonify
from catboost import CatBoostClassifier
import joblib
import pandas as pd

from preprocessing import GBMCategoricalPreparer  # noqa: F401 (needed for joblib.load)

MODEL_PATH = "artifacts/models/catboost_final_v1.cbm"
PREPROCESSOR_PATH = "artifacts/models/preprocessor_catboost_v1.pkl"

# Section 11: cost-optimized decision threshold, fixed on out-of-fold predictions
THRESHOLD = 0.39

app = Flask("hotel_cancellation_prediction")

print("Loading model and preprocessor...")
model = CatBoostClassifier()
model.load_model(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)
print("Model and preprocessor loaded successfully.")


@app.route("/predict", methods=["POST"])
def predict():
    reservation = request.get_json()

    X = pd.DataFrame([reservation])
    X_prep = preprocessor.transform(X)

    probability = model.predict_proba(X_prep)[:, 1][0]
    will_cancel = bool(probability >= THRESHOLD)

    result = {
        "cancellation_probability": round(float(probability), 4),
        "will_cancel": will_cancel,
        "threshold_used": THRESHOLD,
    }

    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)