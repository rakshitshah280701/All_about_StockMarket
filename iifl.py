import urllib

from bs4 import BeautifulSoup
import requests
import re
from datetime import date
from datetime import datetime, timedelta


def iifl_news():
    try:
        date_today = date.today()

        date_yestarday = date.today() - timedelta(1)
        date_before_yestarday = date.today() - timedelta(2)

        if datetime.today().weekday() <= 4:
            url = f"https://www.indiainfoline.com/markets/live-news/{date_today}/Live-News-Sensex-Nifty-live-stock-markets-bse-nse-futures-and-options-derivative-trading"

        elif datetime.today().weekday() == 5:
            url = f"https://www.indiainfoline.com/markets/live-news/{date_yestarday}/Live-News-Sensex-Nifty-live-stock-markets-bse-nse-futures-and-options-derivative-trading"

        elif datetime.today().weekday() == 6:
            url = f"https://www.indiainfoline.com/markets/live-news/{date_before_yestarday}/Live-News-Sensex-Nifty-live-stock-market-bse-nse-futures-and-options-derivative-trading"

        news = requests.get(url)
        doc = BeautifulSoup(news.text, "html.parser")


        headings = list()
        # GET ALL HEADINGS IN TEXT STORED IN LIST
        for updates in doc.find_all("h2", attrs={"class": "fw500 fs20e blue_text"}):
            headings.append(updates.text)

        # print("UPDATES = ", headings)

        # GET ALL STORY CARDS (UPDATES) FROM THE PAGE
        links = doc.find("div", attrs={"class": "story_card h_auto"})

        click_link = list()
        # EXTRACT LINKS FROM THE STORY CARDS
        for l in links.find_all('a', attrs={'href': re.compile("^https://")}):
            if l.get('href').endswith('html'):
                click_link.append(l.get('href'))


        # print("LINKS = ", click_link)

        # TEXT AND LINKS COMBINED INTO A DICTIONARY
        headings_links = dict(zip(headings, click_link))
        limitedIifl = dict(list(headings_links.items())[:25])
        return limitedIifl
    except Exception as e:
        return {}

if __name__ == "__main__":

    print(limitedIifl)
