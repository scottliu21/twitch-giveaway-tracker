from Util.InternetRelatedThread import InternetRelatedThread

class JSONDecoder:
    headers = {'Accept': 'application/vnd.twitchtv.v5+json'}
    channelBadge = 'https://badges.twitch.tv/v1/badges/channels/channelID/display'
    CLIENT_ID = "w07tun6ja438fsymn61ei88tm8kw7q"

    def __init__(self):
        JSONDecoder.headers['Client-ID'] = JSONDecoder.CLIENT_ID
        self.internetRelatedThread = InternetRelatedThread(JSONDecoder)



