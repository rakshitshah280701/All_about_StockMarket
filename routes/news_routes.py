# routes/news_routes.py

from flask import Blueprint, render_template
from services.equity_scraper import limited as equity_limited
from services.iifl_scraper import iifl_news
from services.livemint_scraper import headings_links

# Blueprint name and prefix (optional)
news_bp = Blueprint("news", __name__)

# Homepage
@news_bp.route("/")
def home():
    return render_template("index.html")

# EquityBulls news
@news_bp.route("/equitybulls")
def equitybulls():
    return render_template("newsEquity.html", limited=equity_limited)

# IIFL news
@news_bp.route("/iifl")
def iifl():
    return render_template("newsIifl.html", limitedIifl=iifl_news())

# Livemint news
@news_bp.route("/livemint")
def livemint():
    return render_template("livemint.html", limited=headings_links)
