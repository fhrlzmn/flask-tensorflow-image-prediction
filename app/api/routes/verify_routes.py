from flask import Blueprint, jsonify, request
from app import app
from app.firebase import verify_token
from app.api.middlewares.token_authorization import verify_token_middleware

verify_routes = Blueprint("verify_routes", __name__)


@verify_routes.route("/", methods=["POST"])
@verify_token_middleware
def verify(user_id):
    if user_id:
        return jsonify({"message": "Success", "user_id": user_id}), 200
    else:
        return jsonify({"message": "Invalid token"}), 401  # Unauthorized
