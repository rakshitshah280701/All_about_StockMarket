# services/iifl_scraper.py

import requests
from bs4 import BeautifulSoup

def iifl_news():
    url = "https://www.indiainfoline.com/news"
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, "html.parser")
    news_items = soup.find_all('a')

    headings = []
    links = []

    for item in news_items:
        try:
            if "/article/" in item['href']:
                text = item.text.strip()
                if text and text not in headings:
                    headings.append(text)
                    link = item['href']
                    if not link.startswith("http"):
                        link = "https://www.indiainfoline.com" + link
                    links.append(link)
        except Exception:
            pass

    return dict(zip(headings[:10], links[:10]))
