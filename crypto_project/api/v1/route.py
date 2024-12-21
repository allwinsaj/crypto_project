import json
import threading

from flasgger import swag_from
from flask import Blueprint
from flask import request

from crypto_project.api.common.utils import RestResponses
from crypto_project.api.common.utils import authenticate
from crypto_project.api.v1.actions import CoinDetails
from crypto_project.api.v1.actions import User

coinapp = Blueprint('coinapp', __name__, template_folder='templates')

authapp = Blueprint('authapp', __name__, template_folder='templates')


@authapp.post("/v1/signup")
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'description': 'Request payload to create a user',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Username for the new user',
                        'example': 'john_doe'
                    },
                    'email': {
                        'type': 'string',
                        'description': 'Email address for the new user',
                        'example': 'john.doe@example.com'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password for the new user',
                        'example': 'SecurePassword123'
                    }
                },
                'required': ['username', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Success message',
                        'example': 'User Created Successfully'
                    },
                    'data': {
                        'type': 'object',
                        'properties': {
                            'user_id': {
                                'type': 'string',
                                'description': 'Unique identifier for the newly created user',
                                'example': '60e8c6a94f1d3c4b1c8e4b2f'
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message',
                        'example': 'Invalid input data'
                    }
                }
            }
        }
    }
})
def user_signup():
    req_body = json.loads(request.get_data())
    user = User()
    return user.signup_user(req_body)


@authapp.post("/v1/auth/login")
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'description': 'Log in user',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': 'Login Username',
                        'example': 'john_doe'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Login password',
                        'example': 'Secure@123'
                    }
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Success message',
                        'example': 'User Created Successfully'
                    },
                    'data': {
                        'type': 'object',
                        'properties': {
                            'username': {
                                'type': 'string',
                                'description': 'Unique identifier for the newly created user',
                                'example': 'allwin'
                            },
                            'auth_token': {
                                'type': 'string',
                                'description': 'Auth token to access the apis',
                                'example': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNhaiIsImV4cCI6MTczNDY5MjEzNX0.y_d9WqJFReF3g8RIBAgohfNRRa7_utddBGeeiBhNCmE'
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message',
                        'example': 'Invalid input data'
                    }
                }
            }
        }
    }
})
def user_login():
    req_body = json.loads(request.get_data())
    user = User()
    return user.user_login_user(req_body)


@coinapp.get("/v1/data_refresh")
@swag_from({
    'responses': {
        200: {
            'description': 'Success message indicating that the data refresh process has started.',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Success message',
                        'example': 'Data refresh process started. Check logs for details.'
                    }
                }
            }
        },
        500: {
            'description': 'Internal Server Error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message',
                        'example': 'An error occurred while starting the data refresh process.'
                    }
                }
            }
        }
    }
})
def data_refresh():
    # Run the `data_refresh` function in a separate thread
    coin_details = CoinDetails()
    thread = threading.Thread(target=coin_details.data_refresh, daemon=True)
    thread.start()
    # Return success response immediately
    return RestResponses.success("Data refresh process started. Check logs for details.")


@coinapp.get("/v1/coins")
@authenticate
@swag_from({
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'description': 'Bearer token for authentication',
            'required': True,
            'type': 'string'
        },
        {
            'name': 'limit',
            'in': 'query',
            'description': 'Number of coins to retrieve',
            'required': False,
            'type': 'integer',
            'example': 10
        },
        {
            'name': 'page',
            'in': 'query',
            'description': 'Page number for pagination',
            'required': False,
            'type': 'integer',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'A list of coins',
            'headers': {
                'Content-Type': {
                    'type': 'application/json',
                    'description': 'Content Type header indicating the format of the response'
                },
                'Authorization': {
                    'type': 'string',
                    'description': 'Bearer token for authentication'
                }
            },
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'coin_id': {'type': 'string', 'description': 'Coin ID'},
                        'name': {'type': 'string', 'description': 'Coin\'s name'},
                        'symbol': {'type': 'string', 'description': 'Coin\'s symbol'},
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'description': 'Error message'}
                }
            }
        }
    }
})
def get_coins_list():
    req_args = request.args.to_dict()
    coin_details = CoinDetails()
    return coin_details.get_coins_list(req_args)


@coinapp.get("/v1/coins/categories")
@authenticate
@swag_from({
    'responses': {
        200: {
            'description': 'A list of categories',
            'headers': {
                'Content-Type': {
                    'type': 'string',
                    'description': 'Content Type header indicating the format of the response (e.g., application/json)'
                },
                'Authorization': {
                    'type': 'string',
                    'description': 'Bearer token for authentication'
                }
            },
            'schema': {
                'type': 'object',
                'properties': {
                    'categories': {
                        'type': 'array',
                        'description': 'List of categories',
                        'items': {
                            'type': 'string',
                            'description': 'A category name'
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'description': 'Error message'}
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'description': 'Bearer token for authentication',
            'required': True,
            'type': 'string'
        },
    ]})
def get_coin_categories():
    coin_details = CoinDetails()
    return coin_details.get_coin_categories()


@coinapp.post("/v1/specific_coins")
@authenticate
@swag_from({
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'description': 'Bearer token for authentication',
            'required': True,
            'type': 'string'
        },
        {
            'name': 'body',
            'in': 'body',
            'description': 'Request payload for filtering and pagination',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'filters': {
                        'type': 'object',
                        'description': 'Filters to apply to the list of coins',
                        'example': {
                            'categories': ['Cryptocurrency'],
                            'coin_ids': ["bitcoin"]
                        },
                        'additionalProperties': {
                            'oneOf': [
                                {'type': 'string'},
                                {'type': 'number'},
                                {'type': 'object'}
                            ]
                        }
                    },
                    'page': {
                        'type': 'integer',
                        'description': 'Page number for pagination',
                        'example': 1
                    },
                    'limit': {
                        'type': 'integer',
                        'description': 'Number of items per page',
                        'example': 10
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'A paginated list of coins with details',
            'headers': {
                'Content-Type': {
                    'type': 'string',
                    'description': 'Content Type header indicating the format of the response (application/json)'
                },
                'Authorization': {
                    'type': 'string',
                    'description': 'Bearer token for authentication'
                }
            },
            'schema': {
                'type': 'object',
                'properties': {
                    'page': {
                        'type': 'integer',
                        'description': 'Current page number'
                    },
                    'total_pages': {
                        'type': 'integer',
                        'description': 'Total number of pages available'
                    },
                    'total_items': {
                        'type': 'integer',
                        'description': 'Total number of items available'
                    },
                    'coins': {
                        'type': 'array',
                        'description': 'List of coins on the current page',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'coin_id': {
                                    'type': 'string',
                                    'description': 'Unique identifier for the coin'
                                },
                                'name': {
                                    'type': 'string',
                                    'description': 'Name of the coin'
                                },
                                'categories': {
                                    'type': 'array',
                                    'description': 'List of categories associated with the coin',
                                    'items': {
                                        'type': 'string',
                                        'description': 'A category'
                                    }
                                },
                                'current_price_cad': {
                                    'type': 'number',
                                    'description': 'Current price of the coin in CAD',
                                    'format': 'float'
                                }
                            }
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message'
                    }
                }
            }
        }
    }
})
def specific_coins_details():
    req_body = json.loads(request.get_data())
    coin_details = CoinDetails()
    return coin_details.specific_coins_details(req_body)
