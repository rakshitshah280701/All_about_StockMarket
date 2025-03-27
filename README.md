# 📈 All_about_StockMarket

A Flask web app that predicts the next trading day's stock price using an LSTM model and displays a dynamic candlestick chart for selected stocks.

---

## 🔧 Features

- Predicts stock price for next trading day
- Dynamic candlestick chart (last 60 days)
- Stock symbol dropdown (NSEI, TCS, Infosys, Reliance)
- Modular structure using Flask Blueprints

---

## 🧠 Tech Stack

- **Backend**: Flask, TensorFlow/Keras, yfinance, sklearn
- **Frontend**: HTML, CSS, JS, Plotly
- **Model**: LSTM (saved in `/storage/exported_model`)

---

## ▶️ Run Locally

```bash
git clone <repo_url>
cd All_about_StockMarket
pip install -r requirements.txt
python app.py

```
## Structure

- services/       # Prediction logic (model_predictor.py)
- routes/         # Flask route handlers
- templates/      # HTML templates (predict.html)
- static/         # CSS/JS/Images
- app.py          # App entrypoint
- result.json     # Stores latest prediction
