import json
import os
import sys
print("&&&&&&&&&&&&&&&&")
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# def ensure_path_in_sys_path(project_path):
#     """
#     Ensure the absolute path of the project is in sys.path.
#     If not, append it to sys.path.
#
#     :param project_path: The path of the project to check and append if necessary.
#     """
#     print("*****************")
#     abs_path = os.path.abspath(project_path)
#     print(f"Checking if {abs_path} is in sys.path...")
#
#     if abs_path not in sys.path:
#         print("Adding project path to sys.path...")
#         sys.path.append(abs_path)
#     else:
#         print("Project path already in sys.path.")
#
#     print("Current sys.path:")
#     print(sys.path)  # Print the current sys.path to see if the path was added
#     print("Lastttttttttttttttttttttttttt")
#
# # Call this at the start of your test setup
# ensure_path_in_sys_path(os.path.abspath('.'))
# print("Doneeeeeeeeeeeeeeeeeeeeeeee")

#
# from tests.common.definitions import test_category_data
# from tests.common.definitions import test_coin_collection_data

# def test_get_items(client, mock_mongo, test_coin_collection_data, test_category_data):
#     assert 1==1
#     # Mock MongoDB collection's find method
#     print("_________________")
#     mock_mongo.find.return_value = [test_coin_collection_data]
#
#     # Send GET request to the /items endpoint
#     response = client.get("/v1/coins/categories")
#     json_response = json.loads(response.data)
#     assert response.status_code == 200
#     assert type(json_response) is list
#     assert len(json_response) == 1
#     assert response.json == test_category_data
from tests.common.randomfun import test_category_data
def test_fun():
    assert 1==1