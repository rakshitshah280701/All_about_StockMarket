import os
import json
import traceback
import numpy as np
import keras
import tensorflow as tf
import yfinance as yf
from datetime import date
from sklearn.preprocessing import MinMaxScaler

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(ROOT_PATH, '..', 'storage', 'exported_model')
RESULT_PATH = os.path.join(ROOT_PATH, '..', 'result.json')
print("MODEL_PATH:", MODEL_PATH)

today = date.today()

if len(tf.config.experimental.list_physical_devices('GPU')) < 1:
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def stockReader(stock, start, end):
    return yf.download(stock, start=start, end=end)

def ModelPredictor(symbol='^NSEI', start_date='2018-01-01') -> float:
    try:
        if symbol != '^NSEI':
            raise Exception("Model currently supports only NSEI (^NSEI)")

        if os.path.exists(RESULT_PATH):
            with open(RESULT_PATH, 'r') as f:
                readObject = json.load(f)
                if readObject.get('date') == str(today):
                    return float(readObject.get('result'))

        loaded_model = keras.models.load_model(MODEL_PATH)

        df = stockReader(symbol, start=start_date, end=today)
        close_prices = df['Close'].to_frame()

        last_60_days = close_prices[-60:].values

        scaler = MinMaxScaler(feature_range=(0, 1))
        last_60_days_scaled = scaler.fit_transform(last_60_days)

        X_test = np.array([last_60_days_scaled])  # shape (1, 60, 1)
        prediction = loaded_model.predict(X_test)

        predicted_price = scaler.inverse_transform(prediction)[0][0]

        with open(RESULT_PATH, 'w') as f:
            json.dump({"result": str(predicted_price), "date": str(today)}, f)

        return round(predicted_price, 2)

    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        traceback.print_exc()
        return -1.0
