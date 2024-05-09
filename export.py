import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
# ACCOUNT-V1 URL
REGION_URL = 'https://asia.api.riotgames.com'
# MATCH-V5 SEA URL
MATCH_REGION_URL = 'https://sea.api.riotgames.com'

request_url = f"{REGION_URL}/riot/account/v1/accounts/by-riot-id/proxysinged/oce?api_key={API_KEY}"
response = requests.get(request_url)

# Grab PUUID from in game name + tag
# To be replaced with user input
if response.status_code == 200:
    data = response.json()
    puuid = data['puuid']
    gameName = data['gameName']
    tagLine = data['tagLine']

    print("PUUID:", puuid)
    print("Game Name:", gameName)
    print("Tag Line:", tagLine)
else:
    print("Error:", response.status_code)

