import json
import requests

## To use -> replace [Client-ID] with your client ID and gameName with whatever game you want.

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


## Gets the ID of the game you're looking for by the title of the game (ID needed for the API)
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
        channels[streamer['user_name']] = {'viewers': streamer['viewer_count'], 'title': streamer['title'].strip()}

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
         channels[streamer['user_name']] = {'viewers': streamer['viewer_count'], 'title': streamer['title'].strip()}
    return channels


## Function Calls
gameID = getGameID(gameName)
channels = getListofStreams(gameID)

## Prints the list of channels
for x in channels:
    print(x)
