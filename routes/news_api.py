# routes/news_api.py
from flask import Blueprint, jsonify
import requests
import os

news_api = Blueprint('news_api', __name__)

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY") or "pub_78056d199f51e959f06a8baa99fef48f26b81"

@news_api.route("/api/news")
def get_newsdata():
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q=stock market&country=in&category=business&language=en"
    try:
        res = requests.get(url, timeout=10)
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
        print("[NEWS ERROR]", e)
        return jsonify({"error": "News fetch failed", "data": []}), 500
