from .predict_routes import predict_bp
from .news_routes import news_bp  # for /news route
from .chart_routes import chart_bp
from .news_api import news_api

def register_blueprints(app):
    app.register_blueprint(news_bp, url_prefix="/news")         # ➕ Add this
    app.register_blueprint(news_api)     # ✔ already registered
    app.register_blueprint(predict_bp)
    app.register_blueprint(chart_bp)
