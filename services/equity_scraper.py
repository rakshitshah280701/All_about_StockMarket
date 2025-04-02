# services/equity_scraper.py

import requests
from bs4 import BeautifulSoup

def get_equity_news():
    url = "https://www.equitybulls.com/"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        news_items = soup.select("a.news")
        headlines = []
        links = []

        for item in news_items[:10]:
            title = item.get_text(strip=True)
            href = item.get("href")
            if href and not href.startswith("http"):
                href = "https://www.equitybulls.com/" + href
            headlines.append({"title": title, "link": href})

        print("✅ EquityBulls headlines fetched:", len(headlines))
        return headlines

    except Exception as e:
        print("❌ EquityBulls Scraper Error:", e)
        return []
