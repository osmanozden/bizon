from flask import abort
from flask import current_app
from flask_login import current_user
from functools import wraps
import jwt
import base64

from core.config import config

__all__ = ["verify_jwt_token", "generate_jwt_token", "roles_required"]

RE_JWT = r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$"


def resolve_jwt_token(token) -> dict:

    try:
        return jwt.decode(token, key=config.SECRET_KEY, algorithms=["HS256"])

    except jwt.DecodeError:
        import traceback

        print(traceback.format_exc())
        pass
    return None


def generate_jwt_token(user_id) -> str:
    return jwt.encode({"user_id": user_id}, key=config.SECRET_KEY, algorithm="HS256")


def roles_required(roles):
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            if not current_user.has_roles(roles):
                return abort(403)
            return f(*args, **kwargs)

        return inner

    return wrapper
