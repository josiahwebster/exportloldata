import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
# ACCOUNT-V1 URL
REGION_URL = 'https://asia.api.riotgames.com'
# MATCH-V5 SEA URL
MATCH_REGION_URL = 'https://sea.api.riotgames.com'

# grab puuid from name + tag
def grabID(gamename, tag):
    request_url = f"{REGION_URL}/riot/account/v1/accounts/by-riot-id/{gamename}/{tag}?api_key={API_KEY}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        puuid = data['puuid']
        gameName = data['gameName']
        tagLine = data['tagLine']
    else:
        print("Error Grabbing ID, check user name or tag:", response.status_code)

    return puuid

def grabMatchID(startTime, endTime, queue, type, start, count):
        id = grabID("proxysinged", "oce")

        if id: 
            request_url = f"{MATCH_REGION_URL}/lol/match/v5/matches/by-puuid/{id}/ids?start={startTime}&count={count}&api_key={API_KEY}"
            print(request_url)
            response = requests.get(request_url)

            if response.status_code == 200:
                data=response.json()
                matches=data
                print(matches)
            else:
                print("Error grabbing matches:", response.status_code)

grabMatchID(0, 0, 0, 0, 0, 20)