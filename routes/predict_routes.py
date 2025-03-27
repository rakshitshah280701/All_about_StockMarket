from flask import Blueprint, render_template, request, jsonify
from services.model_predictor import ModelPredictor

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict")
def predict():
    symbol = request.args.get("symbol", "^NSEI")
    return render_template("predict.html", symbol=symbol)

@predict_bp.route("/api/predict")
def api_predict():
    symbol = request.args.get("symbol", "^NSEI")
    result = ModelPredictor(symbol)
    return jsonify({"result": result})
