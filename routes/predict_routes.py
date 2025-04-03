import logging
from flask import Blueprint, render_template, request, jsonify
from services.ml.model_predictor import predict_stock

predict_bp = Blueprint("predict", __name__)

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 1. Frontend route — Renders the UI page
@predict_bp.route("/predict")
def predict():
    return render_template("predict.html")

# 🔹 2. API route — Handles AJAX prediction logic
@predict_bp.route("/api/predict")
def predict_api():
    symbol = request.args.get("symbol", "").strip()
    if not symbol:
        return jsonify({"error": "No stock symbol provided."}), 400

    try:
        result = predict_stock(symbol)
        return jsonify({
            "symbol": result["symbol"],
            "predicted_close": result["predicted_close"],
            "predicted_for": result["predicted_for"]
        })

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    
    except Exception as e:
        print(f"❌ Unhandled Error: {e}")
        return jsonify({"error": "Server error while predicting. Try again."}), 500

