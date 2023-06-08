from flask import Blueprint, jsonify, request
from app import app
from app.utils.predict_image import predict_image
from app.api.middlewares.token_authorization import verify_token_middleware
from app.api.cloud_storage import upload_file
from werkzeug.utils import secure_filename
import os
import datetime

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


predict_routes = Blueprint("predict_routes", __name__)


@predict_routes.route("/", methods=["GET", "POST"]) # type: ignore
@verify_token_middleware
def predict(user_id):
    if user_id is None:
        return jsonify({"message": "Unauthorized"}), 401
    else:
        if request.method == "GET":
            return jsonify({"message": f"Hello, {user_id}"}), 200
        elif request.method == "POST":
            if "image" not in request.files:
                return jsonify({"message": "No file part in the request"}), 400

            file = request.files["image"]

            if file.filename == "":
                return jsonify({"message": "No file selected for uploading"}), 400

            if file and allowed_file(file.filename):
                file_path = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    + "_"
                    + secure_filename(file.filename), # type: ignore
                )
                file.save(file_path)
                result = predict_image(file_path)

                image_url = upload_file(file_path, user_id)

                os.remove(file_path)
                return (
                    jsonify(
                        {"message": "Success", "result": result, "imageUrl": image_url}
                    ),
                    200,
                )
