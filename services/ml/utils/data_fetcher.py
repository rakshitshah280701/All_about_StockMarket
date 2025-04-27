# import yfinance as yf
# import os
# import pandas as pd
# from datetime import datetime

# DATA_DIR = "data/raw"

# def fetch_stock_data(symbol: str, start: str = "2018-01-01", end: str = None) -> pd.DataFrame:
#     if not os.path.exists(DATA_DIR):
#         os.makedirs(DATA_DIR)

#     if end is None:
#         end = datetime.today().strftime('%Y-%m-%d')

#     print(f"Downloading {symbol} from {start} to {end}...")

#     df = yf.download(symbol, start=start, end=end, group_by="column", auto_adjust=True, progress=False)

#     # FORCE flattening (finally kills all weird shapes)
#     if isinstance(df.columns, pd.MultiIndex):
#         df.columns = df.columns.get_level_values(0)

#     df.dropna(inplace=True)
#     df.to_csv(f"{DATA_DIR}/{symbol.replace('^', '').replace('.', '_')}.csv")

#     return df


import yfinance as yf
import os
import pandas as pd
from datetime import datetime

DATA_DIR = "storage/raw"  # or use "storage/raw" if that's your folder

def fetch_stock_data(symbol: str, start: str = None, end: str = None) -> pd.DataFrame:
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # 🗓 Default range = 3 years if nothing passed
    if end is None:
        end = datetime.today()
    if start is None:
        start = end - pd.DateOffset(years=5)

    print(f"⏳ Downloading {symbol} from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}...")

    df = yf.download(symbol, start=start, end=end, group_by="column", auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"❌ No data fetched for symbol {symbol}. Check if the symbol is valid.")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.dropna(inplace=True)
    df.to_csv(f"{DATA_DIR}/{symbol.replace('^', '').replace('.', '_')}.csv")

    return df