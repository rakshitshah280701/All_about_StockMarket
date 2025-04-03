# import os
# import pandas as pd
# import numpy as np
# from datetime import datetime, timedelta
# from tensorflow.keras.models import load_model
# from services.ml.utils.data_fetcher import fetch_stock_data
# from services.ml.utils.indicators import add_technical_indicators
# from services.ml.utils.scaler import scale_dataframe, load_scaler, save_scaler
# from services.ml.utils.windowizer import create_sequences
# from services.ml.trainers.gru_trainer import build_gru_model, train_gru_model


# # Paths
# RAW_DATA_DIR = "storage/raw"
# SAVED_MODEL_DIR = "storage/exported_model"
# SCALER_DIR = "storage/scalers"

# # Helper paths
# def get_data_path(symbol):
#     return os.path.join(RAW_DATA_DIR, f"{symbol}.csv")

# def get_model_path(symbol):
#     return os.path.join(SAVED_MODEL_DIR, f"{symbol}_gru.keras")

# def get_scaler_path(symbol):
#     return os.path.join(SCALER_DIR, f"{symbol}_scaler.pkl")

# # Fetch recent historical stock data
# def get_recent_data(symbol, years=3):
#     end_date = datetime.today()
#     start_date = end_date - timedelta(days=365 * years)
#     return fetch_stock_data(symbol, start=start_date, end=end_date)

# # Prepare data pipeline
# def prepare_data(df, window_size=30):
#     df_ind = add_technical_indicators(df)
#     df_scaled, scaler = scale_dataframe(df_ind)
#     X, y = create_sequences(df_scaled, window_size)
#     return df_scaled, X, y, scaler

# # Main function
# def predict_stock(symbol, window_size=30):
#     model_path = get_model_path(symbol)
#     scaler_path = get_scaler_path(symbol)
#     csv_path = get_data_path(symbol)

#     if os.path.exists(model_path) and os.path.exists(scaler_path):
#         print(f"🔁 Loading model and scaler for {symbol}")
#         model = load_model(model_path)
#         scaler = load_scaler(scaler_path)

#         df = pd.read_csv(csv_path, index_col="Date", parse_dates=True)
#         df_ind = add_technical_indicators(df)
#         df_scaled, _ = scale_dataframe(df_ind, scaler=scaler)

#         # 🔐 Ensure same features and order
#         try:
#             df_scaled = df_scaled.loc[:, scaler.feature_names_in_]
#         except Exception as e:
#             print("⚠️ Feature mismatch. Retraining the model...")
#             os.remove(model_path)
#             os.remove(scaler_path)
#             return predict_stock(symbol, window_size)
#     else:
#         print(f"📈 Training new model for {symbol}")
#         df = get_recent_data(symbol)
#         os.makedirs(RAW_DATA_DIR, exist_ok=True)
#         df.to_csv(csv_path)

#         df_scaled, X, y, scaler = prepare_data(df, window_size=window_size)
#         model, history, _ = train_gru_model(X, y, model_save_path=model_path)

#         os.makedirs(SCALER_DIR, exist_ok=True)
#         save_scaler(scaler, scaler_path)

#     # ✅ Final window for prediction
#     # Drop the 'Close' column just like in training
#     X_pred_window = df_scaled.drop(columns=["Close"]).iloc[-window_size:].values


#     if len(X_pred_window) < window_size:
#         raise ValueError("Not enough recent data to make prediction.")

#     X_pred = np.expand_dims(X_pred_window, axis=0)

#     print("✅ Model expected input shape:", model.input_shape)
#     print("🧪 X_pred shape:", X_pred.shape)
#     print("🧾 df_scaled columns:", df_scaled.columns.tolist())
#     print("🧾 scaler.feature_names_in_:", scaler.feature_names_in_.tolist())
#     print("🧮 Number of features in df_scaled:", df_scaled.shape[1])


#     # 🧠 Predict scaled close price
#     scaled_prediction = model.predict(X_pred)[0][0]

#     # 🎯 Inverse scale only close price
#     # 🎯 Inverse scale only close price
#     close_idx = list(scaler.feature_names_in_).index("Close")
#     padded_input = np.zeros((1, len(scaler.feature_names_in_)))
#     padded_input[0, close_idx] = scaled_prediction

#     descaled_prediction = scaler.inverse_transform(padded_input)[0][close_idx]


#     print(f"📊 Scaled predicted close price for {symbol}: {scaled_prediction:.4f}")
#     print(f"📈 Descaled (actual) predicted close price for {symbol}: ₹{descaled_prediction:.2f}")

#     return {
#         "symbol": symbol,
#         "scaled_prediction": float(scaled_prediction),
#         "predicted_close": float(descaled_prediction),
#         "model_path": model_path,
#         "scaler_path": scaler_path
#     }


# # Run prediction from terminal
# if __name__ == "__main__":
#     symbol = "INFIBEAM.NS"
#     prediction = predict_stock(symbol)
#     print(f"📊 Predicted scaled close price for {symbol}: {prediction}")


import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  # Add at the top

from tensorflow.keras.models import load_model
from services.ml.utils.data_fetcher import fetch_stock_data
from services.ml.utils.indicators import add_technical_indicators
from services.ml.utils.scaler import scale_dataframe, load_scaler, save_scaler
from services.ml.utils.windowizer import create_sequences
from services.ml.trainers.gru_trainer import build_gru_model, train_gru_model


RAW_DATA_DIR = "storage/raw"
SAVED_MODEL_DIR = "storage/exported_model"
SCALER_DIR = "storage/scalers"

def get_data_path(symbol):
    return os.path.join(RAW_DATA_DIR, f"{symbol}.csv")

def get_model_path(symbol):
    return os.path.join(SAVED_MODEL_DIR, f"{symbol}_gru.keras")

def get_scaler_path(symbol):
    return os.path.join(SCALER_DIR, f"{symbol}_scaler.pkl")

def get_recent_data(symbol, years=5):
    end_date = datetime.today()
    start_date = end_date - relativedelta(years=years)  # Fix year subtraction
    return fetch_stock_data(symbol, start=start_date, end=end_date)

def prepare_data(df, window_size=30):
    print(f"🧾 Raw data shape: {df.shape}")
    df_ind = add_technical_indicators(df)
    print(f"📊 After adding indicators: {df_ind.shape}")
    df_scaled, scaler = scale_dataframe(df_ind)
    print(f"📈 After scaling: {df_scaled.shape}")
    X, y = create_sequences(df_scaled, window_size)
    print(f"🧪 After windowing: X={X.shape}, y={y.shape}")
    return df_scaled, X, y, scaler

def get_next_market_day_from_last_data(last_date):
    next_day = last_date + timedelta(days=1)
    while next_day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        next_day += timedelta(days=1)
    return next_day.strftime("%A, %Y-%m-%d")  # e.g., "Monday, 2025-04-07"



def predict_stock(symbol, window_size=30):
    model_path = get_model_path(symbol)
    scaler_path = get_scaler_path(symbol)
    csv_path = get_data_path(symbol)

    # 💡 Check if all components exist
    model_exists = os.path.exists(model_path)
    scaler_exists = os.path.exists(scaler_path)
    csv_exists = os.path.exists(csv_path)

    print(f"📦 Model: {model_exists}, Scaler: {scaler_exists}, CSV: {csv_exists}")

    if model_exists and scaler_exists and csv_exists:
        print(f"🔁 Loading model, scaler, and CSV for {symbol}")
        model = load_model(model_path)
        scaler = load_scaler(scaler_path)

        df = pd.read_csv(csv_path, index_col="Date", parse_dates=True)
        df_ind = add_technical_indicators(df)
        df_scaled, _ = scale_dataframe(df_ind, scaler=scaler)

        try:
            df_scaled = df_scaled.loc[:, scaler.feature_names_in_]
        except Exception as e:
            print("⚠️ Feature mismatch. Retraining the model...")
            os.remove(model_path)
            os.remove(scaler_path)
            return predict_stock(symbol, window_size)

    else:
        print(f"📈 Training new model for {symbol}")
        df = get_recent_data(symbol)
        if df.empty:
            raise ValueError(f"❌ No data for {symbol}.")
        if len(df) < (window_size * 2):  # Require at least 2x window size
            raise ValueError(f"❌ Insufficient data ({len(df)} rows). Need {window_size * 2}.")
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        df.to_csv(csv_path)

        df_scaled, X, y, scaler = prepare_data(df, window_size=window_size)

        if len(X) < 10:
            raise ValueError(f"❌ Not enough training samples for {symbol}. Only got {len(X)}.")

        os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
        model, history, _ = train_gru_model(X, y, model_save_path=model_path)
        print(f"✅ Model trained and saved at {model_path}")

        os.makedirs(SCALER_DIR, exist_ok=True)
        save_scaler(scaler, scaler_path)
        print(f"💾 Scaler saved at {scaler_path}")

    last_available_date = df.index[-1]
    predicted_date = get_next_market_day_from_last_data(last_available_date)

    # ✅ Final prediction
    X_pred_window = df_scaled.drop(columns=["Close"]).iloc[-window_size:].values

    if len(X_pred_window) < window_size:
        raise ValueError("❌ Not enough recent data to make prediction.")

    X_pred = np.expand_dims(X_pred_window, axis=0)

    print("✅ Model expected input shape:", model.input_shape)
    print("🧪 X_pred shape:", X_pred.shape)
    print("🧾 df_scaled columns:", df_scaled.columns.tolist())
    print("🧾 scaler.feature_names_in_:", scaler.feature_names_in_.tolist())
    print("🧮 Number of features in df_scaled:", df_scaled.shape[1])

    scaled_prediction = model.predict(X_pred)[0][0]

    close_idx = list(scaler.feature_names_in_).index("Close")
    padded_input = np.zeros((1, len(scaler.feature_names_in_)))
    padded_input[0, close_idx] = scaled_prediction

    descaled_prediction = scaler.inverse_transform(padded_input)[0][close_idx]

    print(f"📊 Scaled predicted close price for {symbol}: {scaled_prediction:.4f}")
    print(f"📈 Descaled (actual) predicted close price for {symbol}: ₹{descaled_prediction:.2f}")
    

    return {
        "symbol": symbol,
        "scaled_prediction": float(scaled_prediction),
        "predicted_close": float(descaled_prediction),
        "predicted_for": predicted_date,
        "model_path": model_path,
        "scaler_path": scaler_path
    }

# if __name__ == "__main__":
#     symbol = "INFIBEAM.NS"
#     prediction = predict_stock(symbol)
#     print(f"📊 Final prediction for {symbol}: {prediction}")
