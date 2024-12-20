import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from crypto_project.api.v1.actions import CoinDetails, DatabaseAdapter  # Adjust import path accordingly
possible_top_dir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_top_dir, 'crypto_project', '__init__.py')):
    sys.path.insert(0, possible_top_dir)
class TestCoinDetails(unittest.TestCase):

    def setUp(self):
        self.coin_details = CoinDetails()
        self.mock_db = MagicMock(spec=DatabaseAdapter)
        self.coin_details.db = self.mock_db

    def test_get_coins_list_success(self):
        # Prepare mock data
        self.mock_db.get_count.return_value = 100
        self.mock_db.find_documents.return_value = [{"coin_id": "1", "symbol": "BTC", "name": "Bitcoin"}]

        req_args = {'page': 1, 'limit': 10}
        response = self.coin_details.get_coins_list(req_args)

        # Check that the mock methods were called correctly
        self.mock_db.get_count.assert_called_once_with({})
        self.mock_db.find_documents.assert_called_once_with({}, include_fields=["coin_id", "symbol", "name"],
                                                            exclude_fields=["_id"], skip_val=0, limit=10)

        # Assert the response
        self.assertEqual(response['message'], "Coins list fetched successfully")
        self.assertTrue("coins" in response['data'])
        self.assertEqual(len(response['data']['coins']), 1)
        self.assertEqual(response['data']['coins'][0]['coin_id'], "1")

    def test_get_coins_list_failure(self):
        # Simulate an error in the db call
        self.mock_db.get_count.side_effect = Exception("Database error")

        req_args = {'page': 1, 'limit': 10}
        response = self.coin_details.get_coins_list(req_args)

        # Assert the response for error
        self.assertEqual(response['message'], "An error occurred while fetching the coins list")

    def test_get_coin_categories_success(self):
        # Mock category data
        self.mock_db.get_distinct.return_value = ["Bitcoin", "Ethereum"]

        response = self.coin_details.get_coin_categories()

        # Assert the response
        self.assertEqual(response['message'], "Categories retrieved Successfully")
        self.assertTrue("categories" in response['data'])
        self.assertEqual(response['data']['categories'], ["Bitcoin", "Ethereum"])

    def test_specific_coins_details_success(self):
        # Mock data
        self.mock_db.get_count.return_value = 2
        self.mock_db.find_documents.return_value = [{"coin_id": "1", "name": "Bitcoin", "categories": ["crypto"],
                                                     "market_data": {"current_price": {"cad": 50000}}}]

        req_body = {
            "filters": {"coin_ids": ["1"], "categories": ["crypto"]},
            "page": 1,
            "limit": 10
        }

        response = self.coin_details.specific_coins_details(req_body)

        # Assert the response
        self.assertEqual(response['message'], "Coins details fetched successfully")
        self.assertTrue("data" in response)
        self.assertEqual(len(response['data']), 1)
        self.assertEqual(response['data'][0]['coin_id'], "1")
        self.assertEqual(response['data'][0]['current_price_cad'], 50000)

    def test_data_refresh_success(self):
        # Mock requests.get response
        with patch('requests.get') as mock_get:  # Correct patching location
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = [{"id": "1", "name": "Bitcoin"}]
            self.mock_db.update_document = MagicMock()  # Mock update_document method

            response = self.coin_details.data_refresh()

            # Assert the response
            self.assertEqual(response['message'], "Data refresh completed successfully")
            self.mock_db.update_document.assert_called_once_with({"coin_id": "1"},
                                                                 {"$set": {"id": "1", "name": "Bitcoin"}}, upsert=True)

    def test_data_refresh_failure(self):
        # Mock requests.get to simulate failure
        with patch('requests.get') as mock_get:  # Correct patching location
            mock_get.return_value.status_code = 500

            response = self.coin_details.data_refresh()

            # Assert the response for error
            self.assertEqual(response['message'], "Data refresh failed due to an error")


if __name__ == '__main__':
    unittest.main()
