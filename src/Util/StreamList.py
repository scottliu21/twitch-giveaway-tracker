import json
import requests
import re

## to use -> replace [Client-ID] with your client id.

## Parameters to use when your Query the API
## Headers include your client ID / Oauth
## Parameters include name of game or other strings as required by the API

headers = {
    'Client-ID': '[Client-ID]',
}
params = (
    ('name', "World of Warcraft"),
)
channels = {}

## Gets the ID of the game you're looking for by the title of the game
## Sends a API request to twitch to get the game ID by passing in game name as a parameter
response = requests.get('https://api.twitch.tv/helix/games', headers=headers, params=params)
games = json.loads(response.text)
print("Game Title: ", (games['data'][0]['name']))
gameID = games['data'][0]['id']


## Lists all of the channels in a directory (first loop to get the cursor to use for pagination)
## Gets a list of the first 100 streamers in a category then returns a cursor, which you use as a parameter in following
## requests to get the next 100 results, until there are no results remaining
response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params=(('game_id', gameID),('first', 100),))
streamData = json.loads(response.text)
cursor = streamData['pagination']['cursor']
streamersList = streamData['data']
for streamer in streamersList:
    channels[streamer['user_name']] = streamer['title']


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
        channels[streamer['user_name']] = streamer['title']

## Prints the usernames of all live channels in the category
for x in channels:
    print(x)

print(len(channels), "channels")
