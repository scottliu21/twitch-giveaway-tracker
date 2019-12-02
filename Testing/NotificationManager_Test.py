import sys
import os
import time
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from Util.NotificationManager import NotificationManager
from Util.SettingManager import SettingManager


def test_moveUpByOne(tmpdir):
    p = tmpdir.join("NotificationSetting")
    p.write("Consolas\n10\n#ffff7f\n#000000\n\n")
    SettingManager.NOTIFICATION_SETTING_FILE = tmpdir + "\\NotificationSetting"
    manager = NotificationManager(Fake_ChatScreen())
    dialog1 = Fake_NotificationDialog(1)
    dialog2 = Fake_NotificationDialog(2)
    dialog3 = Fake_NotificationDialog(3)
    dialog4 = Fake_NotificationDialog(4)
    manager.notifications.append(dialog1)
    manager.notifications.append(dialog2)
    manager.notifications.append(dialog3)
    manager.notifications.append(dialog4)
    manager.closeNotification(2)
    assert dialog1.moveUpCalled == False and dialog2.moveUpCalled == False and dialog3.moveUpCalled == True and dialog4.moveUpCalled == True, "move up by one test failed"

def test_fadeOutCalled(tmpdir):
    p = tmpdir.join("NotificationSetting")
    p.write("Consolas\n10\n#ffff7f\n#000000\n\n")
    SettingManager.NOTIFICATION_SETTING_FILE = tmpdir + "\\NotificationSetting"
    manager = NotificationManager(Fake_ChatScreen())
    dialog2 = Fake_NotificationDialog(1)
    dialog2.closeTime = time.time() + 9000
    manager.addToSchedule(dialog2)
    time.sleep(1)
    assert dialog2.fadeOutCalled == False, "fade out called test failed"


class Fake_ChatScreen(object):
    def __init__(self):
        self.chatUI = self
        self.centralWidget = self
        self.mainWindow = self

    def setStyleSheet(self, _):
        pass


class Fake_NotificationDialog(object):
    def __init__(self, assignID):
        self.moveUpCalled = False
        self.fadeOutCalled = False
        self.assignID = assignID

    def __eq__(self, other):
        return self.assignID == other

    def moveUpByOne(self):
        self.moveUpCalled = True

    def fadeOut(self):
        self.fadeOutCalled = True