from Util.InternetRelatedThread import InternetRelatedThread

class JSONDecoder:
    headers = {'Accept': 'application/vnd.twitchtv.v5+json'}
    channelBadge = 'https://badges.twitch.tv/v1/badges/channels/channelID/display'
    def __init__(self):
        file = open('setting/clientID', 'r')
        JSONDecoder.headers['Client-ID'] = file.readline()
        file.close()
        self.internetRelatedThread = InternetRelatedThread(JSONDecoder)



