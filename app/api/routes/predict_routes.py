from flask import Blueprint, jsonify, request
from app import app
from app.utils.predict_image import predict_image
from werkzeug.utils import secure_filename
import os
import datetime

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


predict_routes = Blueprint("predict_routes", __name__)


@predict_routes.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return jsonify({"message": "Hello, Predict"}), 200
    elif request.method == "POST":
        if "file" not in request.files:
            return jsonify({"message": "No file part in the request"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"message": "No file selected for uploading"}), 400

        if file and allowed_file(file.filename):
            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                + "_"
                + secure_filename(file.filename),
            )
            file.save(file_path)
            result = predict_image(file_path)
            os.remove(file_path)
            return jsonify({"message": "Success", "result": result}), 200
