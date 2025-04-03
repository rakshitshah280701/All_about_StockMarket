from flask import Blueprint, render_template
from services.equity_scraper import get_equity_news
from services.iifl_scraper import iifl_news as get_iifl_news
from services.livemint_scraper import headings_links as livemint_news

news_bp = Blueprint("news", __name__)

@news_bp.route("/")
def show_news():
    return render_template("news_combined.html")
