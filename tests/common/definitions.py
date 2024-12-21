import pytest
from unittest.mock import MagicMock, patch
from crypto_project.coinapp import coinapp as app


@pytest.fixture
def app_client():
    app.testing = True
    with app.test_client() as client:
        yield client

# @pytest.fixture
# def mock_coin_collection_mongo(mocker):
#     mock_collection = MagicMock()
#     mock_db = {"coin_details": mock_collection}
#     mock_client = MagicMock()
#     mock_client.__getitem__.side_effect = lambda name: mock_db[name]
#     mocker.patch("app.MongoClient", return_value=mock_client)
#     return mock_collection




@pytest.fixture()
def test_category_data():
    return {
        "data": {
            "categories": ["Masternodes"]
        },
        "message": "Categories retrieved Successfully",
        "status": "success"
    }

@pytest.fixture()
def test_coin_collection_data():
    return {
        "coin_id": "01coin",
        "market_data": {
            "current_price": {
                "aed": 0.00071975,
                "ars": 0.200269,
                "aud": 0.00031458,
                "bch": 0.000000501305,
                "bdt": 0.02350712,
                "bhd": 0.00007391,
                "bmd": 0.00019596,
                "bnb": 0.000000316645,
                "brl": 0.00119645,
                "btc": 0.000000002124,
                "cad": 0.00028195
            }
        },
        "name": "01coin",
        "categories": ["Masternodes"]
    }
