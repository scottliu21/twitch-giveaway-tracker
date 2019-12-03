import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from Util.MessageProcessor import MessageProcessor
# Wei-Chieh Hung

# This tests the constructEmoteArray function in MessageProcessor
# This function is convert string provided by Twitch into list of positions to be replaced by emote
# No error handling is tested since the message is parsed from raw Twitch IRC Message, and this function would never be called if it was not parsed
# E.Q. Class            Descriptions                                         Possible Values
# EC_single             A single emote with/without multiple occurrences     test 1 and 2
# EC_none               No emote                                             emotes=
# EC_multiple           Multiple emotes with/without multiple occurrences    test 4
def test_constructEmoteArray():
    actual = MessageProcessor.constructEmoteArray("emotes=354:0-4")
    assert actual == [['354', 0, 4]], "construct emote array test failed"
    actual = MessageProcessor.constructEmoteArray("emotes=354:0-4,18-22,45-49,73-77,93-97,114-118")
    assert actual == [['354', 0, 4], ['354', 18, 22], ['354', 45, 49], ['354', 73, 77], ['354', 93, 97], ['354', 114, 118]], "construct emote array test failed"
    actual = MessageProcessor.constructEmoteArray("emotes=")
    assert actual == [], "construct emote array test failed: empty set"
    actual = MessageProcessor.constructEmoteArray("emotes=354:0-4,18-22/10:45-49/20:73-77,93-97/90:114-118")
    assert actual ==  [['354', 0, 4], ['354', 18, 22], ['10', 45, 49], ['20', 73, 77], ['20', 93, 97], ['90', 114, 118]], "construct emote array test failed: multiple emotes"


# This tests the processMessage function in MessageProcessor
# This function is called to convert raw IRC message from Twitch to HTML escaped strings that can show emotes, user text color and badges in our program
# E.Q. Class            Descriptions                                                    Possible Values
# EC_NoBadgeMessage     Regular raw irc message without the badge tag                   Any regular twitch irc without badges
# EC_Localization       Regular raw irc message with user having non-english names      twitch message with localization names
# EC_RegularMessage     Regular raw irc message given by Twitch                         any other regular raw irc message
# EC_CorruptedMessage   Messages that are not twitch irc message                        any other irc message
def test_processMessage():
    processor = MessageProcessor(Fake_JsonDecoder(), 10, Fake_Signal())
    # EC_RegularMessage
    actual = processor.processMessage("21:15:52 @badge-info=subscriber/13;badges=subscriber/12;color=#2E8B57;display-name=DerektheHobo;emotes=;flags=;id=dfd4557f-2f8c-4ffb-ad95-fc52ecee5420;mod=0;room-id=121059319;subscriber=1;tmi-sent-ts=1575263752845;turbo=0;user-id=57453809;user-type= :derekthehobo!derekthehobo@derekthehobo.tmi.twitch.tv PRIVMSG #moonmoon :lets see if the movies good or not", Fake_UserList())
    assert actual == "[21:15:52] <a href=\"derekthehobo\" style=\"text-decoration:none\" style=\"color:#2E8B57\"><b>DerektheHobo: </b></a>lets see if the movies good or not", "message processing test failed"
    # EC_Localization
    actual = processor.processMessage(
        "18:51:20 @badge-info=;badges=;color=#000000;display-name=小俗仔;emotes=;flags=;id=14139bca-c0d2-4b58-8507-47d9c3627be6;mod=0;room-id=67955580;subscriber=0;tmi-sent-ts=1575341481017;turbo=0;user-id=125953917;user-type= :weebchichi!weebchichi@weebchichi.tmi.twitch.tv PRIVMSG #chewiemelodies :poop",
        Fake_UserList())
    assert actual == "[18:51:20] <a href=\"weebchichi\" style=\"text-decoration:none\" style=\"color:#000000\"><b>小俗仔 (weebchichi): </b></a>poop", "message processing test failed: localization"
    # EC_NoBadgeMessage
    actual = processor.processMessage(
        "18:57:11 @badge-info=;badges=;color=#000000;display-name=test;emotes=;flags=;id=858d9df9-7e49-45e3-947a-5ee3040b06da;mod=0;room-id=68373769;subscriber=0;tmi-sent-ts=1575341831909;turbo=0;user-id=58456914;user-type= :test!test@test.tmi.twitch.tv PRIVMSG #weichichi :test",
        Fake_UserList())
    assert actual == "[18:57:11] <a href=\"test\" style=\"text-decoration:none\" style=\"color:#000000\"><b>test: </b></a>test", "message processing test failed: no badge"
    # EC_CorruptedMessage
    actual = processor.processMessage("this is a test message", Fake_UserList())
    assert not actual, "message processing test failed: broken irc message"


# This tests the insertEmote function in MessageProcessor
# This function is called to replace text in the raw IRC message according the list of messages provided by constructEmoteArray, changing from text to picture
# No error handling is tested since the message is parsed from raw Twitch IRC Message, and this function would never be called if it was not parsed
# E.Q. Class            Descriptions                                                    Possible Values
# EC_NoEmote            irc message with no emote to insert                             any string + empty string as second parameter
# EC_Emote              irc message with emote(s) to insert                             any string + emote tag in twitch's raw irc
def test_insertEmote():
    processor = MessageProcessor(Fake_JsonDecoder(), 13, Fake_Signal())
    # EC_Emote
    actual = processor.insertEmote("4Head HELLO 911 ?? 4Head JAKE IS IN MY ROOM ?? 4Head HE HAS A PULSE BOMB ?? 4Head WHATS THAT? ?? 4Head ILL BE OKAY? ?? 4Head", "354:0-4,19-23,47-51,76-80,97-101,119-123")
    assert actual == "<img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> HELLO 911 ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> JAKE IS IN MY ROOM ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> HE HAS A PULSE BOMB ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> WHATS THAT? ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\"> ILL BE OKAY? ?? <img height=\"26\" src=\"cache/354.png\" alt=\"4Head\">", "insert emote test failed"
    # EC_NoEmote
    actual = processor.insertEmote("this is a test message", "")
    assert actual == "this is a test message", "insert emote test failed: no emote"


# This tests the indirect output from to InternetRelatedThread
# This is called when the program cannot find the cache of an emote and need to download it from the internet
# No error handling is tested since the message is parsed from raw Twitch IRC Message, and this function would never be called if it was not parsed
# E.Q. Class            Descriptions                                                    Possible Values
# EC_NoEmote            irc message with no emote to fetch                              any string + empty string as second parameter
# EC_Emote              irc message with emote(s) to insert                             any string + emote tag in twitch's raw irc
def test_insertEmote_fetchEmote():
    fake_jsonDecoder = Fake_JsonDecoder()
    processor = MessageProcessor(fake_jsonDecoder, 13, Fake_Signal())
    processor.insertEmote(
        "CrreamAwk BrokeBack BlargNaut EleGiggle imGlitch MercyWing2 DoritosChip HolidayTree KevinTurtle GayPride LesbianPride LUL PixelBob PipeHype PermaSmug ShazBotstix SMOrc SoonerLater LUL NotATK PopCorn TinyFace WholeWheat UnSane TBAngel",
        "40-47/425618:118-120,180-182/4240:131-138/2113050:168-178/191313:0-8/114738:20-28/87:150-160/52:162-166/111119:199-206/4339:30-38/27509:140-148/724216:191-197/1896:208-217/111792:219-224/143490:226-232/1003189:49-58/40:84-94/1713825:72-82/1064991:96-103/1064988:105-116/1547903:122-129/34875:184-189/4057:10-18/102242:60-70")
    # EC_NoEmote
    assert fake_jsonDecoder.internetRelatedThread.values == [['get_emote', '191313'], ['get_emote', '4057'], ['get_emote', '114738'], ['get_emote', '4339'], ['get_emote', '1003189'], ['get_emote', '102242'], ['get_emote', '1713825'], ['get_emote', '40'], ['get_emote', '1064991'], ['get_emote', '1064988'], ['get_emote', '425618'], ['get_emote', '1547903'], ['get_emote', '4240'], ['get_emote', '27509'], ['get_emote', '87'], ['get_emote', '52'], ['get_emote', '2113050'], ['get_emote', '425618'], ['get_emote', '34875'], ['get_emote', '724216'], ['get_emote', '111119'], ['get_emote', '1896'], ['get_emote', '111792'], ['get_emote', '143490']], "fetching emote test failed"
    fake_jsonDecoder = Fake_JsonDecoder()
    processor = MessageProcessor(fake_jsonDecoder, 13, Fake_Signal())
    processor.insertEmote("This is a test message", "")
    # EC_NoEmote
    assert fake_jsonDecoder.internetRelatedThread.values == [], "fetching emote test failed: No emote"

# This tests the setBadgeIcon function
# This is called when InternetRelatedThread has finished downloading channel badges and is updating it to the processor
# E.Q. Class            Descriptions                                                    Possible Values
# EC_NoBadge            This channel does not have custom badges                        An empty dictionary
# EC_HasBadges          This channel has custom badges for bits and/or subscribers      A Dictionary
def test_setBadgeIcon():
    processor = MessageProcessor(Fake_JsonDecoder(), 13, Fake_Signal())
    # EC_NoBadge
    processor.setBadgesIcon({})
    assert processor.bitsBadge == {} and processor.subBadge == {}, "set badge icon test failed: no badge"
    #EC_HasBadges
    badges = {}
    badges['subscriber'] = {}
    badges['subscriber']['test'] = 'test'
    processor.setBadgesIcon(badges)
    assert processor.subBadge == badges['subscriber'], "set badge icon test failed: sub badges"
    badges['bits'] = {}
    badges['bits']['test'] = 'test'
    processor.setBadgesIcon(badges)
    assert processor.bitsBadge == badges['bits'], "set badge icon test failed: bit badges"
    processor = MessageProcessor(Fake_JsonDecoder(), 13, Fake_Signal())
    processor.setBadgesIcon(badges)
    assert processor.subBadge == badges['subscriber'] and processor.bitsBadge == badges['bits'], "set badge icon test failed"



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

    def connect(self, function):
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
    