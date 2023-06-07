import firebase_admin
from firebase_admin import auth, storage

default_app = firebase_admin.initialize_app()


def verify_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token["uid"]

        return user_id
    except auth.AuthError as error:
        return None
