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
def api_predict():
    symbol = request.args.get("symbol")

    if not symbol:
        logger.warning("🚫 Missing 'symbol' in query params.")
        return jsonify({"error": "Missing required query parameter: 'symbol'"}), 400

    try:
        logger.info(f"🔍 Predicting for symbol: {symbol}")
        result = predict_stock(symbol)
        return jsonify(result)

    except ValueError as ve:
        logger.error(f"🚨 Data error for {symbol}: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.exception(f"💥 Critical error for {symbol}")
        return jsonify({"error": "Internal server error"}), 500
