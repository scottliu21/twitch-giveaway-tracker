import json
import requests
import re

## To use, replace [Client-ID] with your client ID and gameName with whatever game you want.
## Headers include your client ID / Oauth
## Parameters include name of game or other strings as required by the API

ClientID = '[Client-ID]'
gameName = "World of Warcraft"
channels = {}
count = 0

headers = {
    'Client-ID': ClientID,
}
params = (
    ('name', gameName),
)


## Gets the ID of the game you're looking for by the title of the game
## Give the function a gameName and it will return a gameID
def getGameID(gameName):
    response = requests.get('https://api.twitch.tv/helix/games', headers=headers, params=(('name', gameName),))
    games = json.loads(response.text)
    print("Game Title: ", (games['data'][0]['name']))
    gameID = games['data'][0]['id']
    return gameID


## Lists all of the livestreams in a certain category.
## Give the function a gameID and it will return a list of all live channels and their titles.
def getListofStreams(gameID):
    response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params=(('game_id', gameID),('first', 100),))
    streamData = json.loads(response.text)
    cursor = streamData['pagination']['cursor']
    streamersList = streamData['data']
    for streamer in streamersList:
        channels[streamer['user_name']] = streamer['title'].strip()

    ## Loops through to get all of the channels (using pagination) until no channels remain
    while (cursor != -1):
        response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params=(('game_id', gameID),('first', 100), ('after', cursor),))
        streamData = json.loads(response.text)
        if (len(streamData['pagination']) > 0):
            cursor = streamData['pagination']['cursor']
        else:
            cursor = -1
        streamersList = streamData['data']
        for streamer in streamersList:
         channels[streamer['user_name']] = streamer['title'].strip()
    return channels


## Function Calls
gameID = getGameID(gameName)
channels = getListofStreams(gameID)


## Looks through the titles of the streams and prints a list of channels with giveaway in the title
for x in channels:
    if re.search("[Gg][Ii][Vv]", channels[x]):
        print(x)
        count +=1

## Prints the total number of channels, and the number of channels with giveaway in their title
print("\n" + str(len(channels)) + " channels")
print(str(count) + " giveaways")
