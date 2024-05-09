import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
REGION_URL = 'https://asia.api.riotgames.com'


requests.get(REGION_URL + "/riot/account/v1/accounts/by-riot-id/'proxysinged'/oce")

