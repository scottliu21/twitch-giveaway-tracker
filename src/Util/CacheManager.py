import os
import shutil
import requests

class CacheManager:
    EMOTE_PREFIX = "http://static-cdn.jtvnw.net/emoticons/v1/"
    #use setting file
    DIRECTORY = "cache/"

    @staticmethod
    def getEmoteImage(emoteID):
        if not os.path.exists(CacheManager.DIRECTORY + emoteID):
            CacheManager.downloadImage(CacheManager.EMOTE_PREFIX + emoteID + "/1.0", "", emoteID)

    @staticmethod
    def downloadImage(url, subFolder, fileName):
        r = requests.get(url, stream=True)
        with open(CacheManager.DIRECTORY + subFolder + fileName + ".png", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            #get dimension
            #send signal maybe

    @staticmethod
    def getChatBadges(channel, json):
        channel += "/"
        badges = {}
        if json['badge_sets'].get('subscriber', None) is not None:
            if not os.path.exists(CacheManager.DIRECTORY + channel):
                os.mkdir(CacheManager.DIRECTORY + channel)
            badges['subscriber'] = {}
            for badge in json['badge_sets']['subscriber']['versions']:
                badges['subscriber'][badge] = CacheManager.DIRECTORY + channel + badge + ".png"
                CacheManager.downloadImage(json['badge_sets']['subscriber']['versions'][badge]['image_url_1x'], channel, badge)
        if json['badge_sets'].get('bits', None) is not None:
            if not os.path.exists(CacheManager.DIRECTORY + channel):
                os.mkdir(CacheManager.DIRECTORY + channel)
            badges['bits'] = {}
            for badge in json['badge_sets']['bits']['versions']:
                badges['bits'][badge] = CacheManager.DIRECTORY + channel + badge + ".png"
                CacheManager.downloadImage(json['badge_sets']['bits']['versions'][badge]['image_url_1x'], channel, badge)
        return badges

    @staticmethod
    def prepareEmote(emoteID, internetRelatedThread):
        internetRelatedThread.addJob(['get_emote', emoteID])

    @staticmethod
    def clearCache():
        shutil.rmtree(CacheManager.DIRECTORY)
        os.mkdir(CacheManager.DIRECTORY)
