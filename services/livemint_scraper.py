# services/livemint_scraper.py

import requests
from bs4 import BeautifulSoup

url = "https://www.livemint.com/"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, "html.parser")

# All headlines and links
headings = []
links = []

for item in soup.find_all("a"):
    try:
        href = item.get("href", "")
        text = item.get_text(strip=True)

        if "/news/" in href and text and href not in links:
            if not href.startswith("http"):
                href = "https://www.livemint.com" + href
            headings.append(text)
            links.append(href)

    except Exception:
        pass

# Top 10 as a dictionary
headings_links = dict(zip(headings[:10], links[:10]))
