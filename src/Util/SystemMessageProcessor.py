import re
from Util.SystemMessageThread import SystemMessageThread
from GUI.Chat.User import UserListEntry
import random

class SystemMessageProcessor:
    HOST_MODE = re.compile('.*HOSTTARGET #([^ ]+) :([^ ]+)')
    JOIN_MESSAGE = re.compile(':(?P<username>[^!]+)!.* JOIN #(?P<channel>.*)$')
    PART_MESSAGE = re.compile(':(?P<username>[^!]+)!.* PART #(?P<channel>.*)$')
    SUB_MESSAGE = re.compile('.*display-name=(?P<displayName>[^;]*).*;login=(?P<id>[^;]*).*;msg-id=(?P<messageId>[^;]*);msg-param-months=(?P<month>[\d]+).*;msg-param-sub-plan-name=(?P<subPlanName>[^;]+);msg-param-sub-plan=(?P<subPlan>[^;]+).* USERNOTICE #(?P<channelName>[^ ]+).*')
    ROOMSTATE = re.compile('(@broadcaster-lang=([^;]+)?;)?.*emote-only=([01]);.*followers-only=([^;]+);.*r9k=([01]);.*room-id=([^;]+);.*slow=([^;]+);.*subs-only=([01]).*ROOMSTATE #(.*)')
    NOTICE = re.compile('@msg-id=([^ ]+) .*NOTICE #([^ ]+) :(.*)')
    NAME_LIST = re.compile('.* 353 .* #(.*) :(.*)')
    SYSTEM_MODDING = re.compile(':jtv MODE #(.*) \+o (.*)')
    GLOBALUSERSTATE = re.compile('color=([^;]*);display-name=([^;]*).*user-id=([\d]+)')

    def __init__(self, chatScreen):
        self.chatScreen = chatScreen
        self.internetRelatedThread = chatScreen.jsonDecoder.internetRelatedThread
        self.systemMessageThread = SystemMessageThread(self, self.chatScreen)
        self.systemMessageThread.start()
        self.internetRelatedThread.start()

    def processMessage(self, message):
        parsedResult = []
        if ' PART ' in message:
            parsedResult.append("Part")
            result = re.search(SystemMessageProcessor.PART_MESSAGE, message)
            parsedResult.append(result)
            if result.group('username') + '\n' != self.chatScreen.clientIRC.nickname:
                chatTab = self.chatScreen.tabs.get('#' + result.group('channel'))
                if chatTab:
                    if chatTab.userList.nickList.get(result.group('username'), None):
                        chatTab.userList.removeUser(chatTab.userList.nickList[result.group('username')], True)
        elif ' JOIN ' in message:
            parsedResult.append("Join")
            result = re.search(SystemMessageProcessor.JOIN_MESSAGE, message)
            parsedResult.append(result)
            chatTab = self.chatScreen.tabs.get('#' + result.group('channel'))
            chatTab.userList.addUser(result.group('username'))
        elif ' WHISPER ' in message:
            self.chatScreen.newWhisperSignal.emit(message)
        elif ' USERSTATE ' in message:
            pass
        elif ' USERNOTICE ' in message:
            result = re.search(SystemMessageProcessor.SUB_MESSAGE, message)
            if result:
                parsedResult.append("Sub")
                parsedResult.append(result)

        elif ' ROOMSTATE ' in message:
            result = re.search(SystemMessageProcessor.ROOMSTATE, message)
            if result is not None:
                chatTab = self.chatScreen.tabs.get('#' + result.group(9))
                # chatTab.setRoomState(result.group(1), result.group(2), result.group(3), result.group(4),
                #                      result.group(5), result.group(6), result.group(7))
                #change later
                self.internetRelatedThread.addJob(['set_badges', chatTab.channelChat, result.group(6)])
        elif ' +o ' in message:
            result = re.search(SystemMessageProcessor.SYSTEM_MODDING, message)
            userList = self.chatScreen.tabs.get('#' + result.group(1)).userList
            userList.reIndexUserForSystemModding(result.group(2))
        elif ' 353 ' in message:
            result = re.search(SystemMessageProcessor.NAME_LIST, message)
            userList = self.chatScreen.tabs.get('#' + result.group(1)).userList
            for nick in result.group(2).split(' '):
                if userList.nickList.get(nick, None) is None:
                    userList.addUser(nick)
        elif ' HOSTTARGET ' in message:
            result = re.search(SystemMessageProcessor.HOST_MODE, message)
        elif 'GLOBALUSERSTATE' in message:
            result = re.search(SystemMessageProcessor.GLOBALUSERSTATE, message)
            if result.group(1):
                self.chatScreen.clientIRC.userColor = result.group(1)
            else:
                self.chatScreen.clientIRC.userColor = random.choice(UserListEntry.DEFAULT_COLOR)
            if result.group(2):
                if (any(not character.isalpha() and not character.isdigit() for character in result.group(2))):
                    self.chatScreen.clientIRC.userDisplayName = result.group(2) + ' (' + self.chatScreen.clientIRC.nickname + ')'
                else:
                    self.chatScreen.clientIRC.userDisplayName = result.group(2)
            else:
                self.chatScreen.clientIRC.userDisplayName = self.chatScreen.clientIRC.nickname
            self.chatScreen.clientIRC.userID = result.group(3)
        else:
            print(message)


