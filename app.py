# app.py

from flask import Flask
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
