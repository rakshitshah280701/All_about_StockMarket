# from flask import Blueprint, request, jsonify
# import json
# from pathlib import Path

# symbols_api = Blueprint('symbols_api', __name__)

# # Update the path to point to scripts/data
# try:
#     with open(Path('scripts/data/nse_symbols.json')) as f:
#         SYMBOLS = json.load(f)
#     print(f"Loaded {len(SYMBOLS)} symbols successfully")
# except FileNotFoundError:
#     print("Warning: nse_symbols.json not found in scripts/data/. Symbol search will not work.")
#     SYMBOLS = []
# except json.JSONDecodeError:
#     print("Warning: nse_symbols.json is not valid JSON. Symbol search will not work.")
#     SYMBOLS = []

# @symbols_api.route('/api/symbols')
# def get_symbols():
#     q = request.args.get('q', '').upper()
#     if len(q) < 1:
#         return jsonify([])
    
#     results = []
#     for symbol in SYMBOLS:
#         if (q in symbol['symbol'].upper() or 
#             q in symbol['name'].upper()):
#             results.append(symbol)
#             if len(results) >= 10:  # Limit to 10 results
#                 break
    
#     return jsonify(results)

from flask import Blueprint, request, jsonify
import json
from pathlib import Path
import sys
import os

symbols_api = Blueprint('symbols_api', __name__)

def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        return Path(sys._MEIPASS)
    else:
        # Running in normal Python environment
        return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Update the path to point to scripts/data
try:
    symbols_path = get_base_path() / 'scripts' / 'data' / 'nse_symbols.json'
    with open(symbols_path) as f:
        SYMBOLS = json.load(f)
    print(f"✅ Loaded {len(SYMBOLS)} symbols successfully from {symbols_path}")
except FileNotFoundError:
    print(f"❌ Warning: nse_symbols.json not found at {symbols_path}. Symbol search will not work.")
    SYMBOLS = []
except json.JSONDecodeError:
    print("❌ Warning: nse_symbols.json is not valid JSON. Symbol search will not work.")
    SYMBOLS = []

@symbols_api.route('/api/symbols')
def get_symbols():
    q = request.args.get('q', '').upper()
    if len(q) < 1:
        return jsonify([])
    
    results = []
    for symbol in SYMBOLS:
        if (q in symbol['symbol'].upper() or 
            q in symbol['name'].upper()):
            results.append(symbol)
            if len(results) >= 10:  # Limit to 10 results
                break
    
    return jsonify(results)