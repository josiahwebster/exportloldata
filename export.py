import requests
import os
from dotenv import load_dotenv
import time
import pandas as pd
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

# Grab matches from user ID
def grabMatchID(startTime, endTime, queue, type, start, count):
        id = grabID("proxysinged", "oce")

        if id: 
            request_url = f"{MATCH_REGION_URL}/lol/match/v5/matches/by-puuid/{id}/ids?startTime={startTime}&type={type}&start={start}&count={count}&api_key={API_KEY}"
            response = requests.get(request_url)

            if response.status_code == 200:
                data=response.json()
                return data
                
            else:
                print("Error grabbing matches:", response.status_code)

# Grab match info
# Participant = 10 users in a given match
def grabMatchInfo(matchID):
    id = grabID("proxysinged", "oce")

    request_url = f"{MATCH_REGION_URL}/lol/match/v5/matches/{matchID}?api_key={API_KEY}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        
        if 'info' in data and 'participants' in data['info']:
            participants = data['info']['participants']
            participantData = findUserData(data, id)
            return participantData
            if participantData:
                print("Participant data found")
            else:
                print("Participant not found in this match")
        else:
            print("Match information not found in the response.")
    else:
        print("Error grabbing match data:", response.status_code)

# Scrape response for specific participants data (the user we are interested in)
def findUserData(data, userID):
        participant_data = None
        for participant in data['info']['participants']:
            if participant['puuid'] == userID:
                participant_data = participant
                return participant_data
        print("User is not in the given match")
        return 0

# Grab users data for 100 games at a time (max api call)
# use variable cycle to persist until the match history is exhausted
# only includes ranked matches from the current season (hardcoded as Jan 9 2024)
def grabCurrentSeasonData():
    # Jan 9, 2024 season start 
    # 6 required parameters according to API
    seasonStartDate = '1704805200'
    currentDate = time.time()
    queue = ''
    gameType = 'ranked'
    start = 0
    count = 100
    # cycle variable
    cycle = 0

    data = pd.DataFrame(columns=['MatchID', 'Win', 'Duration', 'Kills', 'Deaths', 'Assists', 'Damage Dealt to Champions'])

    for x in range (50):
        matchID = grabMatchID(seasonStartDate, currentDate, queue, gameType, cycle * 100, count)
        # print(matchID)
        for i in range(0, len(matchID)):
            if matchID[i] != 0:
                matchInfo = grabMatchInfo(matchID[i])
                gameResult = matchInfo['win']
                gameDuration = matchInfo['timePlayed']
                playerKills = matchInfo['kills']
                playerDeaths = matchInfo['assists']
                playerAsissts = matchInfo['deaths']
                playerDamage = matchInfo['totalDamageDealtToChampions']
                data.loc[i + (cycle * count)] = [matchID[i], gameResult, gameDuration, playerKills, playerDeaths, playerAsissts
                                                 , playerDamage]
            
            if matchID[i] == 0:
                print("Match history exhausted")
                return 0
        cycle += 1
        
    df = pd.DataFrame(data)
    print(df) 
    file_name = 'lolData.xlsx'
    data.to_excel(file_name)
        
grabCurrentSeasonData()
