import requests
import threading
from queue import Queue
from Util.CacheManager import CacheManager

class InternetRelatedThread(threading.Thread):

    def __init__(self, JSONDecoder):
        super().__init__(target=self.run)
        self.jsonDecoder = JSONDecoder
        self.queuedCall = Queue()
        self.setDaemon(True)
        self.setName('InternetRelatedThread')

    def addJob(self, call):
        self.queuedCall.put(call)

    def run(self):
        while True:
            event = self.queuedCall.get()
            if event[0] == 'get_emote':
                CacheManager.getEmoteImage(event[1])
            elif event[0] == 'set_badges':
                badges = CacheManager.getChatBadges(event[1].channelName, requests.get(self.jsonDecoder.channelBadge.replace('channelID', event[2]), headers=self.jsonDecoder.headers).json())
                event[1].messageProcessor.setBadgesIcon(badges)