# CONFIGURATION FILE

import os

DEFAULT_SHOP_URL = "https://sklep000000.shoparena.pl" # Good practice is to use technical domain
DEFAULT_API_USER = "admin"
DEFAULT_API_PASSWORD = "test"
DEFAULT_TOKEN = "" 

SHOP_CURRENCY = "PLN" # Example: "PLN", "EUR"
DEFAULT_LOCALE = "pl_PL" # Example: "pl_PL", "en_US", "cs_CZ"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CRAWL_DELAY = 1 # 1 request per second is safe for ShoperSaaS