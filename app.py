# from flask import Flask, redirect
# from routes import register_blueprints

# def create_app():
#     app = Flask(__name__)
#     register_blueprints(app)

   

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     # from services.ml.model_predictor import predict_stock
#     # prediction = predict_stock("INFY.NS")
#     # print("📊 Manual prediction complete:", prediction)
#     app.run(debug=True)

from flask import Flask, redirect, jsonify, render_template
from routes import register_blueprints
import yfinance as yf
import pandas as pd
import requests




def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app

# 👇 Expose app instance globally for gunicorn
app = create_app()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/ticker')
def get_ticker_data():
    
    symbols = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "NASDAQ": "^IXIC",
        "DOW JONES": "^DJI",
        "USD-INR": "USDINR=X"
    }

    data = []
    for name, symbol in symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d", interval="1m")

            if hist.empty:
                raise ValueError("No data")

            latest = hist.iloc[-1]
            previous = hist.iloc[-2] if len(hist) > 1 else latest
            trend = "up" if latest["Close"] > previous["Close"] else "down" if latest["Close"] < previous["Close"] else "flat"

            data.append({
                "name": name,
                "value": f"{latest['Close']:.2f}",
                "trend": trend
            })

        except Exception as e:
            print(f"[ERROR] Failed for {symbol}: {e}")
            data.append({
                "name": name,
                "value": "N/A",
                "trend": "flat"
            })

    return jsonify(data)

@app.route('/api/nse-movers')
def get_nse_movers():
    try:
        # Step 1: List of NIFTY 50 symbols
        nifty50_symbols = [
            "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS",
            "ITC.NS", "LT.NS", "AXISBANK.NS", "KOTAKBANK.NS", "HINDUNILVR.NS", "WIPRO.NS",
            "ONGC.NS", "BAJFINANCE.NS", "MARUTI.NS", "NTPC.NS", "ASIANPAINT.NS", "SUNPHARMA.NS",
             "POWERGRID.NS", "ULTRACEMCO.NS", "HCLTECH.NS", "TITAN.NS", "TECHM.NS",
            "GRASIM.NS", "JSWSTEEL.NS", "BPCL.NS", "CIPLA.NS", "DRREDDY.NS", "HINDALCO.NS"
        ]

        # Step 2: Fetch 1-day historical data for all
        data = yf.download(tickers=" ".join(nifty50_symbols), period="1d", interval="1d", group_by='ticker')

        # Step 3: Build DataFrame of % change
        movers = []
        for symbol in nifty50_symbols:
            try:
                df = data[symbol]
                open_price = df["Open"].values[0]
                close_price = df["Close"].values[0]
                change_pct = ((close_price - open_price) / open_price) * 100
                movers.append({
                    "symbol": symbol.replace(".NS", ""),
                    "price": f"{close_price:.2f}",
                    "change": f"{change_pct:.2f}"
                })
            except Exception as e:
                continue  # Skip broken ones

        # Step 4: Sort and slice top 5
        gainers = sorted(movers, key=lambda x: float(x["change"]), reverse=True)[:5]
        losers = sorted(movers, key=lambda x: float(x["change"]))[:5]

        return jsonify({"gainers": gainers, "losers": losers})

    except Exception as e:
        print("yfinance mover error:", e)
        return jsonify({"gainers": [], "losers": [], "error": str(e)}), 500




# 👇 Local dev mode (ignored by gunicorn on Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
