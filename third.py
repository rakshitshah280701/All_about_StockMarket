from bs4 import BeautifulSoup
import requests

url = "https://www.livemint.com/market/stock-market-news"

news = requests.get(url)
doc = BeautifulSoup(news.text, "html.parser")

headings = []

for updates in doc.find_all("h2", class_="headline"):
    headings.append(updates.text.strip())

#print(headings)

get_href = lambda element: "https://www.livemint.com" + element["href"]
click_link = list(map(get_href, doc.select("h2.headline>a", href=True)))

#print("Links:", click_link)

print("Number of hreadings", len(headings))
#print("Number of links", len(click_link))

headings_links = dict(zip(headings, click_link))
#limitedLM = dict(list(headings_links.items()))[:20]

#print(headings_links)