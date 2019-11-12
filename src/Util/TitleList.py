import json
import requests
import re

## To use -> Replace [Client-ID] with your client id and "fortnite" with any category title.

## Parameters to use when your Query the API
## Headers include your client ID / Oauth
## Parameters include name of game or other strings as required by the API

headers = {
    'Client-ID': '[Client-ID]',
}
params = (
    ('name', "Fortnite"),
)
channels = {}
count = 0

## Gets the ID of the game you're looking for by the title of the game
response = requests.get('https://api.twitch.tv/helix/games', headers=headers, params=params)
games = json.loads(response.text)
print("Game Title: ", (games['data'][0]['name']))
gameID = games['data'][0]['id']

## Lists the top 100 live streamers in that game category
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

## Looks through the titles of the streams and prints a list of channels with giveaway in the title
for x in channels:
    if re.search("[Gg][Ii][Vv]", channels[x]):
        print(x)
        count +=1

## Prints the total number of channels, and the number of channels with giveaway in their title
print("\n",len(channels), "channels")
print("", count, "giveaways")
