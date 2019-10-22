import re
import html
from Util.CacheManager import CacheManager

class MessageProcessor:
    EMOTE_PATTERN = re.compile('(\d+):(\d+-\d+,?)+')
    EMOTE_RANGE = re.compile('((\d+)-(\d+)),?')
    EMOTE_PREFIX = 'http://static-cdn.jtvnw.net/emoticons/v3/'
    MESSAGE_PATTERN = re.compile('(?P<time>\d\d:\d\d:\d\d).*badges=(?P<badges>[^;]*);(?P<bits>bits=(?P<bitsAmount>\d+).*)?color=(?P<color>[^;]*);.*display-name=(?P<displayname>(?P<displaynameOtherLanguage>[^A-Za-z]*)|(?P<displaynameCapitalization>[^;]*));.*emotes=(?P<emotes>[^;]*);.*user-id=(?P<userID>\d+);.*:(?P<username>[^!]+)!.*#(?P<channel>[^ ]+) :(?P<action> ACTION )?(?P<message>.*)')
    INTERNET_RELATED_THREAD = None
    IMAGE_SIZE = ""
    BADGE_SIZE =""

    HTML_ESCAPE_TABLE = {"&": "&amp;", '"': "&quot;", "'": "&apos;", ">": "&gt;", "<": "&lt;", }
    def __init__(self, jsonDecoder, imgSize):
        self.jsonDecoder = jsonDecoder
        MessageProcessor.INTERNET_RELATED_THREAD = jsonDecoder.internetRelatedThread
        self.bitsBadge = {}
        self.subBadge = {}
        #to be changed to using image cache later
        MessageProcessor.IMAGE_SIZE = 'height="' + str(int(imgSize*2)) + '"'
        MessageProcessor.BADGE_SIZE = 'height="' + str(int(imgSize*1.5)) + '"'

    def processMessage(self, response, channelChat, userList):
        message = re.search(MessageProcessor.MESSAGE_PATTERN, response)
        print(response)
        print(message)
        if message:
            finalMessage = '[' + message.group('time') + '] '
            nameLink = message.group('username')
            user = userList.nickList.get(nameLink, None)
            if user is None:
                userList.addUser(nameLink)
                user = userList.nickList.get(nameLink)
            if not user.hasSpoken:
                user.hasSpoken = True
                userList.updateUser(user.nick, message.group('badges'), self.subBadge, self.bitsBadge, MessageProcessor.BADGE_SIZE)
                user.updateUserColor(message.group('color'))
            else:
                if user.badges != message.group('badges'):
                    userList.updateUser(user.nick, message.group('badges'), self.subBadge, self.bitsBadge, MessageProcessor.BADGE_SIZE)
            finalMessage += user.badgesImage
            bits = 'group 3, to be done'
            finalMessage += '<a href="' + nameLink + '" style="text-decoration:none" '
            if message.group('color'):
                if user.color != message.group('color') and message.group('color') != "000000":
                    user.updateUserColor(message.group('color'))
            finalMessage += 'style="color:' + user.color + '">'
            if message.group('displayname'):
                if message.group('displaynameOtherLanguage'):
                    displayName = message.group('displaynameOtherLanguage') + ' (' + nameLink + ')'
                else:
                    displayName = message.group('displaynameCapitalization')
            else:
                displayName = nameLink
            displayName = '<b>' + displayName + ': </b></a>'
            finalMessage += displayName
            #if mentioned, elif group 12, also change user name if /me
            userMessage = MessageProcessor.insertEmote(message.group('message'), message.group('emotes'))
            if message.group('action') is not None:
                userMessage = '<font color="' + user.color + '">' + userMessage + "</font>"
            finalMessage += userMessage
            #emotes = to be done
            print(finalMessage)
            channelChat.newMessage(finalMessage)


    @staticmethod
    def insertEmote(message, emotes):
        if emotes == '':
            return html.escape(message, MessageProcessor.HTML_ESCAPE_TABLE)
        finalMessage = ''
        emoteArray = MessageProcessor.constructEmoteArray(emotes)
        slicingIndex = 0
        for emote in emoteArray:
            CacheManager.prepareEmote(emote[0], MessageProcessor.INTERNET_RELATED_THREAD)
            finalMessage += html.escape(message[slicingIndex : emote[1]], MessageProcessor.HTML_ESCAPE_TABLE)
            finalMessage += '<img ' + MessageProcessor.IMAGE_SIZE + ' src="' + CacheManager.DIRECTORY + emote[0] + '.png" alt="' + message[emote[1]:emote[2]+1] + '">'
            slicingIndex = emote[2]+1
        finalMessage += html.escape(message[slicingIndex:], MessageProcessor.HTML_ESCAPE_TABLE)
        return finalMessage

    @staticmethod
    def constructEmoteArray(emote):
        #add bttv and frankerz later
        emoteArray = []
        result = re.search(MessageProcessor.EMOTE_PATTERN, emote)
        while result:
            emoteAndRanges = result.group(0)
            index = 0
            ranges = re.split(MessageProcessor.EMOTE_RANGE, emoteAndRanges)
            for i in range(2, len(ranges), 4):
                for x in range(len(emoteArray), 0, -1):
                    if int(ranges[i+1]) > emoteArray[x-1][2]:
                        index = x
                        break
                emoteArray.insert(index, [ranges[0][0:len(ranges[0]) - 1], int(ranges[i]), int(ranges[i + 1])])
            emote = emote[result.end():]
            result = re.search(MessageProcessor.EMOTE_PATTERN, emote)
        return emoteArray

    def setBadgesIcon(self, badges):
        if badges.get('subscriber', None) is not None:
            for badge in badges['subscriber']:
                self.subBadge[badge] = badges['subscriber'][badge]
        if badges.get('bits', None) is not None:
            for badge in badges['bits']:
                self.bitsBadge[badge] = badges['bits'][badge]
