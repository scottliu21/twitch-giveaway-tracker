import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from Util.MessageProcessor import MessageProcessor


def test_constructEmoteArray():
    actual = MessageProcessor.constructEmoteArray("emotes=354:0-4,18-22,45-49,73-77,93-97,114-118")
    assert all([a == b for a, b in zip(actual, [['354', 0, 4], ['354', 18, 22], ['354', 45, 49], ['354', 73, 77], ['354', 93, 97], ['354', 114, 118]])]), "bitch"


def test_processMessage():
    processor = MessageProcessor(Fake_JsonDecoder(), 10, Fake_Signal)
    actual = processor.processMessage("21:15:52 @badge-info=subscriber/13;badges=subscriber/12;color=#2E8B57;display-name=DerektheHobo;emotes=;flags=;id=dfd4557f-2f8c-4ffb-ad95-fc52ecee5420;mod=0;room-id=121059319;subscriber=1;tmi-sent-ts=1575263752845;turbo=0;user-id=57453809;user-type= :derekthehobo!derekthehobo@derekthehobo.tmi.twitch.tv PRIVMSG #moonmoon :lets see if the movies good or not", Fake_UserList())
    assert actual == "[21:15:52] <a href=\"derekthehobo\" style=\"text-decoration:none\" style=\"color:#2E8B57\"><b>DerektheHobo: </b></a>lets see if the movies good or not", "message processing test failed"


def test_insertEmote():
    processor = MessageProcessor(Fake_JsonDecoder(), 13, Fake_Signal)
    actual = processor.insertEmote("4Head HELLO 911 ?? 4Head JAKE IS IN MY ROOM ?? 4Head HE HAS A PULSE BOMB ?? 4Head WHATS THAT? ?? 4Head ILL BE OKAY? ?? 4Head", "354:0-4,19-23,47-51,76-80,97-101,119-123")
    assert actual == "<img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> HELLO 911 ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> JAKE IS IN MY ROOM ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> HE HAS A PULSE BOMB ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> WHATS THAT? ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> ILL BE OKAY? ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\">", "insert emote test failed"


def test_insertEmote_fetchEmote():
    fake_jsonDecoder = Fake_JsonDecoder()
    processor = MessageProcessor(fake_jsonDecoder, 13, Fake_Signal)
    processor.insertEmote(
        "CrreamAwk BrokeBack BlargNaut EleGiggle imGlitch MercyWing2 DoritosChip HolidayTree KevinTurtle GayPride LesbianPride LUL PixelBob PipeHype PermaSmug ShazBotstix SMOrc SoonerLater LUL NotATK PopCorn TinyFace WholeWheat UnSane TBAngel",
        "40-47/425618:118-120,180-182/4240:131-138/2113050:168-178/191313:0-8/114738:20-28/87:150-160/52:162-166/111119:199-206/4339:30-38/27509:140-148/724216:191-197/1896:208-217/111792:219-224/143490:226-232/1003189:49-58/40:84-94/1713825:72-82/1064991:96-103/1064988:105-116/1547903:122-129/34875:184-189/4057:10-18/102242:60-70")
    assert fake_jsonDecoder.internetRelatedThread.values == [['get_emote', '191313'], ['get_emote', '4057'], ['get_emote', '114738'], ['get_emote', '4339'], ['get_emote', '1003189'], ['get_emote', '102242'], ['get_emote', '1713825'], ['get_emote', '40'], ['get_emote', '1064991'], ['get_emote', '1064988'], ['get_emote', '425618'], ['get_emote', '1547903'], ['get_emote', '4240'], ['get_emote', '27509'], ['get_emote', '87'], ['get_emote', '52'], ['get_emote', '2113050'], ['get_emote', '425618'], ['get_emote', '34875'], ['get_emote', '724216'], ['get_emote', '111119'], ['get_emote', '1896'], ['get_emote', '111792'], ['get_emote', '143490']], "fetching emote test failed"


class Fake_JsonDecoder(object):
    def __init__(self):
        self.internetRelatedThread = Fake_InternetRelatedThread()


class Fake_InternetRelatedThread(object):
    def __init__(self):
        self.values = []

    def addJob(self, job):
        self.values.append(job)


class Fake_Signal(object):
    def __init__(self):
        pass

    def connect(self):
        pass


class Fake_UserList(object):
    def __init__(self):
        self.nickList = {}

    def addUser(self, user):
        userEntry = Fake_UserListEntry(user)
        self.nickList[user] = userEntry
        userEntry.updateUserBadge('', '', '', '')

    def updateUser(self, arg1, arg2, arg3, arg4, arg5):
        pass


class Fake_UserListEntry(object):
    def __init__(self, username):
        self.badges = ''
        self.nick = username
        self.badgesImage = ''
        self.color = ''

    def updateUserColor(self, color):
        self.color = color

    def updateUserBadge(self, arg1, arg2, arg3, arg4,):
        pass

    def hasSpoken(self):
        return False