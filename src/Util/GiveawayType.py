import json
import requests
import re

ClientID = '[Client-ID]'
gameName = "Sample Name"

headers = {
    'Client-ID': ClientID,
}
params = (
    ('name', gameName),
)

class GiveawayType:

    ## Gets the ID of the game you're looking for by the title of the game
    ## Give the function a gameName and it will return a gameID
    def getGameID(gameName):
        response = requests.get('https://api.twitch.tv/helix/games', headers=headers, params=(('name', gameName),))
        games = json.loads(response.text)
        print((games['data'][0]['name']))
        gameID = games['data'][0]['id']
        return gameID

    gameID = getGameID(gameName)

    ##Can use task 2 implementation here to check for bots
    def checkBot(user):
        if user is 'NightBot' or 'StreamElements':
            return True
        else:
            return False

    def analyzeBotMessage(message):

        ##Check for string values between " "
        def findBetween(message):
            botMessage = re.findall('"([^"]*)"', message)
            return botMessage

        ##Python code to find the URL from an input string
        def findURL(message):
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            return url

        ##If no url is found, print only substring between quotations and game category, else print url as well
        if not findURL(message):
            print("Potential giveaway item is" + findBetween(message) + " in the '" + gameName + "' category")
        else:
            print("Potential giveaway item is" + findBetween(message) + " in the '" + gameName + "' category")
            print("Potential giveaway link is: " + findURL(message))









