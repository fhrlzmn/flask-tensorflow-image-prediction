from flask import Flask, jsonify
from flask_cors import CORS

UPLOAD_FOLDER = "temp"

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return jsonify({"message": "Hello, World!"}), 200


from app.api.routes.predict_routes import predict_routes

app.register_blueprint(predict_routes, url_prefix="/api/predict")

# app.config.from_object("app.config.DevelopmentConfig")
