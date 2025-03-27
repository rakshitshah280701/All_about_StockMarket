# routes/__init__.py

from .news_routes import news_bp
from .predict_routes import predict_bp
from .chart_routes import chart_bp
#from .sentiment_routes import sentiment_bp

def register_blueprints(app):
    app.register_blueprint(news_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(chart_bp)
    #app.register_blueprint(sentiment_bp)
