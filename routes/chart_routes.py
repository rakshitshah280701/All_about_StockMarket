# routes/chart_routes.py

from flask import Blueprint, request, jsonify
from services.ml.utils.data_fetcher import fetch_stock_data
from datetime import date, timedelta

chart_bp = Blueprint("chart", __name__)

@chart_bp.route('/get_chart_data', methods=['GET'])
def get_chart_data():
    try:
        symbol = request.args.get("symbol", "^NSEI")
        end_date = date.today()
        start_date = end_date - timedelta(days=90)

        # 📈 Use the modern fetcher
        df = fetch_stock_data(symbol, start=start_date, end=end_date)
        df = df.tail(60)

        data = []
        for index, row in df.iterrows():
            data.append({
                "date": index.strftime('%Y-%m-%d'),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close'])
            })

        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
