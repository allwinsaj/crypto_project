import datetime
import threading
import time

import jwt
import requests
from flask import Flask
from oslo_config import cfg
from oslo_log import log as logging
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import Response

from common.mongo_adapter import DatabaseAdapter
from crypto_project.api.common import utils
from crypto_project.api.common.definitions import Urls
from crypto_project.api.common.utils import RestResponses
from crypto_project.api.common.utils import pagination

data_refresh_lock = threading.Lock()
app = Flask(__name__)
LOG = logging.getLogger(__name__)


class CoinDetails:

    def __init__(self):
        self.db = DatabaseAdapter()

    def get_coins_list(self, req_args: dict) -> Response:
        try:
            total_count = self.db.get_count({})
            page_count = 1
            page = 0
            limit = 0
            skip_val = 0
            if req_args:
                page = int(req_args.get('page', 0))
                limit = int(req_args.get('limit', 0))
                skip_val, limit, page_count = pagination(limit, page, total_count, 1, skip_val=0)

            output = self.db.find_documents({},
                                            include_fields=["coin_id", "symbol", "name"],
                                            exclude_fields=["_id"],
                                            skip_val=skip_val,
                                            limit=limit)
            output = list(output)
            # paginated_output = output[skip_val:skip_val + limit]
            return RestResponses.success("Coins list fetched successfully", data={
                "coins": output,
                "total": total_count,
                "page_count": page_count,
                "current_page": page
            })

        except Exception as e:
            LOG.error(f"Error fetching coins list: {e}")
            return RestResponses.bad_request("An error occurred while fetching the coins list")

    def get_coin_categories(self) -> Response:
        data = self.db.get_distinct("categories", query={})
        return RestResponses.success("Categories retrieved Successfully", data={"categories": data})

    def specific_coins_details(self,
                               req_body: dict):
        filters = req_body.get("filters", {})
        coin_ids = filters.get("coin_ids", [])
        categories = filters.get("categories", [])
        query = {
            "$or": [
                {"coin_id": {"$in": coin_ids}},
                {"categories": {"$in": categories}}
            ]
        }
        page = int(req_body.get('page', 0))
        limit = int(req_body.get('limit', 0))
        total_count = self.db.get_count(query)
        skip_val, limit, page_count = pagination(limit, page, total_count, 1, skip_val=0)
        data = self.db.find_documents(query,
                                      skip_val=skip_val,
                                      limit=limit)
        data = list(data)
        result = []

        for coin in data:
            market_data = coin.get("market_data", {})
            current_price = market_data.get("current_price", {})
            if not current_price:
                continue

            cad_price = current_price.get("cad")
            result.append({
                "coin_id": coin.get("coin_id"),
                "name": coin.get("name"),
                "categories": coin.get("categories"),
                "current_price_cad": cad_price
            })

        return RestResponses.success("Coins details fetched successfull", data=result)

    def data_refresh(self) -> Response:
        with app.app_context():  # Ensure we are in the app context
            try:
                url = Urls.COINS_LIST_URL
                headers = {"accept": "application/json"}

                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    LOG.error("Coins list API failed!")
                    return RestResponses.bad_request("Coins list API failed!")

                for i in response.json():
                    try:
                        coin_id_url = Urls.COIN_ID_URL.format(i['id'])
                        coin_response = requests.get(coin_id_url, headers=headers)

                        # Handle rate limit response
                        if coin_response.status_code == 429:
                            LOG.warning(f"Rate limit hit for coin: {i['id']}. Retrying...")
                            time.sleep(60)
                            coin_response = requests.get(coin_id_url, headers=headers)

                        if coin_response.status_code == 200:
                            coin_data = coin_response.json()
                            self.db.update_document({"coin_id": i["id"]}, {"$set": coin_data}, upsert=True)
                    except Exception as e:
                        LOG.error(f"Error updating coin {i['id']}: {e}")

                LOG.info("Data refresh completed successfully")
                return RestResponses.success("Data refresh completed successfully")

            except Exception as e:
                LOG.error(f"Error during data refresh: {e}")
                return RestResponses.bad_request("Data refresh failed due to an error")


class User:
    def __init__(self):
        self.db = DatabaseAdapter()
        self.db.set_collection_name("user")

    def signup_user(self,
                    req_body) -> Response:
        username = req_body.get('username')
        password = req_body.get('password')
        email = req_body.get('email')

        if not utils.validate_username(username):
            return RestResponses.bad_request("Invalid Username")

        if not utils.validate_email(email):
            return RestResponses.bad_request("Invalid Email!!!")

        if not utils.validate_password(password):
            return RestResponses.bad_request(
                "Invalid Password, Passwords may only contain alphanumeric and special characters (.?!@#$%^&*-), and must start with an alphabetic character as well as include at least one number and special character.")

        query = {
            "username": username,
            "email": email
        }
        if self.db.find_document(query):
            return RestResponses.bad_request("User already Exists")

        doc = {
            "username": username,
            "password": generate_password_hash(password),
            "email": email,
            "status": "active"
        }
        user_id = self.db.insert_document(doc)
        return RestResponses.success("User Created Successfully", data={"user_id": str(user_id.inserted_id)})

    def user_login_user(self,
                        req_body) -> Response:
        username = req_body.get('username')
        password = req_body.get('password')

        user = self.db.find_document({
            "username": username
        })
        if not user or not check_password_hash(user['password'], password):
            return RestResponses.unauthorized("Invalid username or password!")

        # Generate JWT token
        token = jwt.encode({
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        }, cfg.CONF.token.JWT_SECRET_KEY, algorithm="HS256")
        return RestResponses.success("Login successfullu", data={"username": username, "access_token": token})
