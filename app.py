# from flask import Flask, redirect
# from routes import register_blueprints

# def create_app():
#     app = Flask(__name__)
#     register_blueprints(app)

   

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     # from services.ml.model_predictor import predict_stock
#     # prediction = predict_stock("INFY.NS")
#     # print("📊 Manual prediction complete:", prediction)
#     app.run(debug=True)

from flask import Flask, redirect
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app

# 👇 Expose app instance globally for gunicorn
app = create_app()

# 👇 Local dev mode (ignored by gunicorn on Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
