import functools
from typing import Any

import jwt
from flask import make_response
from flask import request
from oslo_config import cfg
from werkzeug.wrappers import Response

from common.mongo_adapter import DatabaseAdapter


class RestResponses:
    @staticmethod
    def success(message: str,
                /,
                *,
                status="success",
                data: Any = None) -> Response:
        body = {
            "status": status,
            "message": message,
            "data": data
        }
        return make_response(body, 200)

    @staticmethod
    def bad_request(message: str,
                    /,
                    *,
                    status="failed",
                    data: Any = None) -> Response:
        body = {
            "status": status,
            "message": message,
            "data": data
        }
        return make_response(body, 400)

    @staticmethod
    def unauthorized(message: str,
                     /,
                     *,
                     status="unauthorized",
                     data: Any = None) -> Response:
        body = {
            "status": status,
            "message": message,
            "data": data
        }
        return make_response(body, 401)


def authenticate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return RestResponses.unauthorized("Invalid User")

        token = auth_header.split(" ")[1]  # Extract token
        try:
            db = DatabaseAdapter()
            db.set_collection_name("user")
            # Decode the JWT token
            payload = jwt.decode(token, cfg.CONF.token.JWT_SECRET_KEY, algorithms=["HS256"])
            username = payload.get("username")

            # Validate user existence in the database
            if not db.find_document({"username": username}):
                return RestResponses.unauthorized("User not found")

            # Pass user info to the protected route
            return func(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return RestResponses.unauthorized("Token has expired")
        except jwt.InvalidTokenError:
            return RestResponses.unauthorized("Invalid token")

    return wrapper
