import json
import requests
import re

## Parameters to use when your Query the API
## Headers include your client ID / Oauth
## Parameters include name of game or other strings as required by the API

headers = {
    'Client-ID': '[Client-ID]',
}
params = (
('name', "Fortnite"),
)

## Gets the ID of the game you're looking for by the title of the game
response = requests.get('https://api.twitch.tv/helix/games', headers=headers, params=params)
games = json.loads(response.text)
print("Game Title: ", (games['data'][0]['name']))
gameID = games['data'][0]['id'];

## Gets a list of the top 100 live streamers in that game category
response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params=(('game_id', gameID),('first', 100),))
streamersList = json.loads(response.text)
streamersList = streamersList['data']

## Prints a list of streamers with giveaway in their title.
print("\nGiveaway Listings: ")
for streamer in streamersList:
    if re.search("[Gg][Ii][Vv]", streamer['title']):
        print(streamer['user_name'].ljust(16), "\n   Viewers: ", streamer['viewer_count'], "\n   Title: ", streamer['title'])
