import json
import requests

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

## Lists the top 100 live streamers in that game category
response = requests.get('https://api.twitch.tv/helix/streams', headers=headers, params=(('game_id', gameID),('first', 100),))
streamersList = json.loads(response.text)
streamersList = streamersList['data']

##Prints the usernames, viewcount and titles of the top 100 streams in a category
print("Top 100 live streams: ")
for streamer in streamersList:
    print("Name:", streamer['user_name'].ljust(16), "Viewers: ",  streamer['viewer_count'],)

##Prints a list of the top 100 streamers of the category (For easy implementation into channel text file)
print("\n")
for streamer in streamersList:
    print(streamer['user_name'])
