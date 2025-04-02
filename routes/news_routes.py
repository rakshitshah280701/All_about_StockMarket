from flask import Blueprint, render_template
from services.equity_scraper import get_equity_news
from services.iifl_scraper import iifl_news as get_iifl_news
from services.livemint_scraper import headings_links as livemint_news

news_bp = Blueprint("news", __name__)

@news_bp.route("/news")
def all_news():
    equity_data = get_equity_news()
    iifl_data = get_iifl_news()

    print("📍 Equity:", equity_data)
    print("📍 IIFL:", iifl_data)
    print("📍 Livemint:", livemint_news)


    return render_template("news_combined.html",
        equity=equity_data,
        iifl=iifl_data,
        livemint=livemint_news
    )

@news_bp.route("/")
def home():
    return render_template("index.html")
