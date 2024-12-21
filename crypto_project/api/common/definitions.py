class Regex(object):
    email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    password = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_+=<>?/.,;:]).+$'
    username = r'^[a-zA-Z0-9_]+$|^[a-zA-Z]+$'

class Urls(object):
    COINS_LIST_URL = "https://api.coingecko.com/api/v3/coins/list"
    COIN_ID_URL = "https://api.coingecko.com/api/v3/coins/{}"