import pandas as pd
import json
from pathlib import Path

def process_symbols():
    # Read the CSV file
    df = pd.read_csv('EQUITY_L.csv')
    
    # Create a list of dictionaries with symbol and name
    symbols = []
    for _, row in df.iterrows():
        symbols.append({
            'symbol': row['SYMBOL'],
            'name': row['NAME OF COMPANY'].strip(),
            'yahoo_symbol': f"{row['SYMBOL']}.NS"  # Adding .NS suffix for Yahoo Finance
        })
    
    # Create data directory if it doesn't exist
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Save to JSON file
    with open(data_dir / 'nse_symbols.json', 'w') as f:
        json.dump(symbols, f, indent=2)
    
    print(f"Processed {len(symbols)} symbols")

if __name__ == "__main__":
    process_symbols()