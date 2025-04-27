# update_models.py
import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import pytz
import schedule
import time
import logging
from pathlib import Path

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now we can import from services
try:
    from services.ml.utils.data_fetcher import fetch_stock_data
    from services.ml.utils.indicators import add_technical_indicators
    from services.ml.utils.scaler import scale_dataframe, save_scaler
    from services.ml.utils.windowizer import create_sequences
    from services.ml.trainers.gru_trainer import train_gru_model
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Current PYTHONPATH: {sys.path}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(project_root, 'model_updates.log')),
        logging.StreamHandler()
    ]
)

# Update paths to be relative to project root
RAW_DATA_DIR = os.path.join(project_root, "storage", "raw")
SAVED_MODEL_DIR = os.path.join(project_root, "storage", "exported_model")
SCALER_DIR = os.path.join(project_root, "storage", "scalers")
SYMBOLS_FILE = os.path.join(project_root, "scripts/data", "nse_symbols.json")

def get_model_path(symbol):
    return os.path.join(SAVED_MODEL_DIR, f"{symbol}_gru.keras")

def get_scaler_path(symbol):
    return os.path.join(SCALER_DIR, f"{symbol}_scaler.pkl")

def prepare_data(df, window_size=30):
    """Prepare data for model training"""
    logging.info(f"Raw data shape: {df.shape}")
    df_ind = add_technical_indicators(df)
    logging.info(f"After adding indicators: {df_ind.shape}")
    df_scaled, scaler = scale_dataframe(df_ind)
    logging.info(f"After scaling: {df_scaled.shape}")
    X, y = create_sequences(df_scaled, window_size)
    logging.info(f"After windowing: X={X.shape}, y={y.shape}")
    return df_scaled, X, y, scaler

def update_model(symbol, window_size=30):
    """Update model for a single symbol"""
    try:
        logging.info(f"Updating model for {symbol}")
        
        # Fetch 5 years of data for training
        end_date = datetime.now(pytz.timezone('Asia/Kolkata'))
        start_date = end_date - timedelta(days=365 * 5)
        
        # Fetch data
        df = fetch_stock_data(symbol, start=start_date, end=end_date)
        if df is None or df.empty:
            logging.error(f"No data found for {symbol}")
            return False
            
        if len(df) < (window_size * 2):
            logging.error(f"Insufficient data for {symbol}: {len(df)} rows")
            return False

        # Prepare data
        df_scaled, X, y, scaler = prepare_data(df, window_size=window_size)
        
        if len(X) < 10:
            logging.error(f"Not enough training samples for {symbol}: {len(X)}")
            return False

        # Save paths
        model_path = get_model_path(symbol)
        scaler_path = get_scaler_path(symbol)
        
        # Create directories if they don't exist
        os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
        os.makedirs(SCALER_DIR, exist_ok=True)
        
        # Train and save model
        model, history, _ = train_gru_model(X, y, model_save_path=model_path)
        logging.info(f"Model trained and saved at {model_path}")
        
        # Save scaler
        save_scaler(scaler, scaler_path)
        logging.info(f"Scaler saved at {scaler_path}")
        
        return True
        
    except Exception as e:
        logging.error(f"Error updating model for {symbol}: {str(e)}")
        return False

def update_all_models():
    """Update all models"""
    try:
        # Load symbols from JSON file
        with open(SYMBOLS_FILE, 'r') as f:
            symbols = pd.read_json(f)
            
        total = len(symbols)
        success = 0
        failed = 0
        
        logging.info(f"Starting update for {total} models")
        
        for idx, row in symbols.iterrows():
            symbol = row['yahoo_symbol']
            if update_model(symbol):
                success += 1
            else:
                failed += 1
                
            # Log progress
            logging.info(f"Progress: {idx+1}/{total} (Success: {success}, Failed: {failed})")
            
        logging.info(f"Update complete. Success: {success}, Failed: {failed}")
        
    except Exception as e:
        logging.error(f"Error in update_all_models: {str(e)}")

def run_scheduled_update():
    """Run the update with logging"""
    logging.info("Starting scheduled model update")
    update_all_models()
    logging.info("Scheduled update complete")

def main():
    # Schedule updates
    # Run at 6:00 PM IST (12:30 UTC) every day
    schedule.every().day.at("12:30").do(run_scheduled_update)
    
    # Also run immediately on start
    run_scheduled_update()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()