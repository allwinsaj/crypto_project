import functools
import re
from typing import Any

import jwt
import requests
from flask import make_response
from flask import request
from oslo_config import cfg
from werkzeug.wrappers import Response

from common.mongo_adapter import DatabaseAdapter
from crypto_project.api.common.definitions import Regex


def pagination(limit: int,
               page: int,
               resource_count: int,
               page_count: int,
               /,
               *,
               skip_val: int = 0) -> tuple[int, int, int]:
    if page:
        if not limit:
            limit = 10
        if resource_count > limit:
            page_count = int(resource_count / limit)
            if resource_count % limit:
                page_count += 1
        if page > page_count:
            raise Exception("Invalid Page Number")
        skip_val = (page - 1) * limit
        if page_count == page:
            limit = resource_count - (page - 1) * limit
    return skip_val, limit, page_count


def get_usd_to_cad_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        rates = response.json().get("rates", {})
        return rates.get("CAD", 1)
    else:
        return 1


def validate_email(email: str) -> bool:
    email_regex = Regex.email
    return bool(re.match(email_regex, email))


def validate_username(username: str) -> bool:
    """Validate the username: 3-20 characters, alphanumeric and underscores."""
    if 3 <= len(username) <= 20:
        username_regex = Regex.username
        return bool(re.match(username_regex, username))

    return False


def validate_password(password: str) -> bool:
    """Validate password: minimum 8 characters, at least one number, one uppercase letter, and one special character."""
    if len(password) >= 8:
        password_regex = Regex.password
        return bool(re.match(password_regex, password))

    return False


class RestResponses:
    @staticmethod
    def success(message: str,
                /,
                *,
                status="success",
                data: Any = None,
                **kwargs) -> Response:
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
                    data: Any = None,
                    **kwargs) -> Response:
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
                     data: Any = None,
                     **kwargs) -> Response:
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
