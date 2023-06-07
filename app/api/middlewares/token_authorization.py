from flask import Flask, request
from functools import wraps
from app import app
from app.firebase import verify_token


def verify_token_middleware(func):
    @wraps(app)
    def wrapper(*args, **kwargs):
        authorization_header = request.headers.get("Authorization")
        id_token = authorization_header.split(" ")[1]

        user_id = verify_token(id_token)

        kwargs["user_id"] = user_id

        return func(*args, **kwargs)

    return wrapper
