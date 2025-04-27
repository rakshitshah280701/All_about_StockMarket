# # routes/news_api.py
# from flask import Blueprint, jsonify
# import requests
# import os
# import json
# from dotenv import load_dotenv

# news_api = Blueprint('news_api', __name__)

# def get_api_key():
#     try:
#         # First try to get from environment variable (development mode)
#         load_dotenv()
#         api_key = os.getenv("NEWSDATA_API_KEY")
#         if api_key:
#             return api_key

#         # If not found in env, try to get from config.json (bundled mode)
#         if getattr(sys, 'frozen', False):
#             # Running in bundled mode
#             bundle_dir = os.path.dirname(sys._MEIPASS)
#         else:
#             # Running in development mode
#             bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
#         config_path = os.path.join(bundle_dir, 'config.json')
#         if os.path.exists(config_path):
#             with open(config_path, 'r') as f:
#                 config = json.load(f)
#                 return config.get('NEWSDATA_API_KEY')
#     except Exception as e:
#         print(f"[CONFIG ERROR] Failed to load API key: {e}")
#     return None

# @news_api.route("/api/news")
# def get_newsdata():
#     api_key = get_api_key()
#     if not api_key:
#         print("[NEWS ERROR] API key not found")
#         return jsonify({"error": "API key not configured", "data": []}), 500

#     url = f"https://newsdata.io/api/1/news?apikey={api_key}&q=stock market&country=in&category=business&language=en"
#     try:
#         print("[NEWS] Attempting to fetch news...")
#         res = requests.get(url, timeout=10)
#         print(f"[NEWS] Response status code: {res.status_code}")
        
#         if res.status_code != 200:
#             print(f"[NEWS ERROR] API response: {res.text}")
#             return jsonify({"error": f"News API returned status {res.status_code}", "data": []}), 500
            
#         data = res.json()
#         if "results" not in data:
#             print(f"[NEWS ERROR] Unexpected API response format: {data}")
#             return jsonify({"error": "Invalid API response format", "data": []}), 500
            
#         news = [
#             {
#                 "title": a["title"],
#                 "link": a["link"],
#                 "source": a.get("source_id", "Unknown"),
#                 "date": a.get("pubDate", "")
#             }
#             for a in data.get("results", [])[:8]  # top 8 headlines
#         ]
#         print(f"[NEWS] Successfully fetched {len(news)} news items")
#         return jsonify(news)
#     except Exception as e:
#         print("[NEWS ERROR]", str(e))
#         return jsonify({"error": f"News fetch failed: {str(e)}", "data": []}), 500

# routes/news_api.py
from flask import Blueprint, jsonify
import requests
import os
import json
import sys

news_api = Blueprint('news_api', __name__)

def get_api_key():
    try:
        if getattr(sys, 'frozen', False):
            # Running in bundled mode
            base_dir = sys._MEIPASS  # This is the correct way!
            print(f"[DEBUG] Running in bundled mode, base dir: {base_dir}")
        else:
            # Running in development mode
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            print(f"[DEBUG] Running in development mode, base dir: {base_dir}")

        config_path = os.path.join(base_dir, 'config.json')
        print(f"[DEBUG] Looking for config.json at: {config_path}")

        if os.path.exists(config_path):
            print("[DEBUG] config.json found")
            with open(config_path, 'r') as f:
                config = json.load(f)
                api_key = config.get('NEWSDATA_API_KEY')
                if api_key:
                    print("[DEBUG] API key found in config.json")
                    return api_key
                else:
                    print("[DEBUG] No API key in config.json")
        else:
            print("[DEBUG] config.json not found")

    except Exception as e:
        print(f"[CONFIG ERROR] Failed to load API key: {str(e)}")
    return None

@news_api.route("/api/news")
def get_newsdata():
    api_key = get_api_key()
    if not api_key:
        print("[NEWS ERROR] API key not found")
        return jsonify({"error": "API key not configured", "data": []}), 500

    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q=stock market&country=in&category=business&language=en"
    try:
        print("[NEWS] Attempting to fetch news...")
        res = requests.get(url, timeout=10)
        print(f"[NEWS] Response status code: {res.status_code}")
        
        data = res.json()
        news = [
            {
                "title": a["title"],
                "link": a["link"],
                "source": a.get("source_id", "Unknown"),
                "date": a.get("pubDate", "")
            }
            for a in data.get("results", [])[:8]  # top 8 headlines
        ]
        return jsonify(news)
    except Exception as e:
        print("[NEWS ERROR]", str(e))
        return jsonify({"error": f"News fetch failed: {str(e)}", "data": []}), 500