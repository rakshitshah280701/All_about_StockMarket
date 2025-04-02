# services/iifl_scraper.py

import requests
from bs4 import BeautifulSoup

def iifl_news():
    url = "https://www.indiainfoline.com/news"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.select("a.news-title")  # adjust this selector based on inspect

        headlines = []
        for tag in articles[:10]:
            title = tag.get_text(strip=True)
            link = tag.get("href")
            if link and not link.startswith("http"):
                link = "https://www.indiainfoline.com" + link
            headlines.append({"title": title, "link": link})

        print("✅ IIFL headlines fetched:", len(headlines))
        return headlines

    except Exception as e:
        print("❌ IIFL Scraper Error:", e)
        return []
