# services/equity_scraper.py

import requests
from bs4 import BeautifulSoup

# Web scraping EquityBulls news
url = "https://www.equitybulls.com/"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
news = soup.find_all('a')

headings = []
links = []

for item in news:
    try:
        if 'newsdet' in item['href']:
            headings.append(item.text.strip())
            links.append(url + item['href'])
    except Exception:
        pass

# Dictionary of news headline -> link
limited = dict(zip(headings[:10], links[:10]))
