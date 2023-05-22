from bs4 import BeautifulSoup
import requests
import re

url = "https://www.equitybulls.com/"

news = requests.get(url)
doc = BeautifulSoup(news.text, "html.parser")

headings = list()
for updates in doc.find_all("div", attrs={"class": "media-body"}):
    headings.append(updates.text)

# print("HEADINGS=", headings)

# links = doc.find("div", attrs={"class": "media-body"})

click_link = list()

for l in doc.find_all(class_="catg_title", href=True):
    l_ck = l.get('href')
    click_link.append("https://www.equitybulls.com/" + l_ck)

# print("Links = ", click_link)

headings_links = dict(zip(headings, click_link))
limited = dict(list(headings_links.items())[:25])

if __name__ == "__main__":
    print(limited)
    print(len(limited))
    # print(headings_links)
    # print(len(headings_links))
