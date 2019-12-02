import sys
import os
import time
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from GUI.SubWindows.NotificationDialog import NotificationDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPoint

font = QFont("Consolas", 10, -1, False)


def test_joinChannel(qtbot):
    fake_notificationManager = Fake_NotificationManager()
    widget = NotificationDialog(1, "test", "testChannel", "testMessage", 1, font, fake_notificationManager)
    qtbot.mouseRelease(widget.label, Qt.RightButton)
    assert fake_notificationManager.channel == "testChannel", "join channel test failed: user right clicked on widget"


def test_closeNotification(qtbot):
    fake_notificationManager = Fake_NotificationManager()
    widget = NotificationDialog(1, "test", "testChannel", "testMessage", 0, font, fake_notificationManager)
    qtbot.mouseRelease(widget.label, Qt.LeftButton)
    assert fake_notificationManager.closeNotificationCalled == True, "close notification test failed: user left clicked on widget"


def test_mouseEntersAndLeaves(qtbot):
    fake_notificationManager = Fake_NotificationManager()
    widget = NotificationDialog(1, "test", "testChannel", "testMessage", 0, font, fake_notificationManager)
    qtbot.addWidget(widget)
    qtbot.mouseMove(widget.label, QPoint(10, 10))
    qtbot.mouseMove(widget.label, QPoint(11, 11), delay=1000)
    assert fake_notificationManager.removeFromScheduleByAssignIDCalled == True, "mouse enter test failed: user's mouse enters the widget"
    qtbot.mouseMove(widget.label, QPoint(-1, 1))
    qtbot.mouseMove(widget.label, QPoint(-2, 1), delay=1000)
    assert fake_notificationManager.addToScheduleCalled == True, "mouse enter test failed: user's mouse leaves the widget"


def test_eqOperator():
    fake_notificationManager = Fake_NotificationManager()
    widget = NotificationDialog(1, "test", "testChannel", "testMessage", 0, font, fake_notificationManager)
    assert widget == 1, "eq operator failed"

class Fake_NotificationManager():
    def __init__(self):
        self.chatScreen = self
        self.chatUI = self
        self.centralWidget = self
        self.mainWindow = None
        self.channel = None
        self.removeFromScheduleByAssignIDCalled = False
        self.notificationHasFadedOutCalled = False
        self.closeNotificationCalled = False
        self.addToScheduleCalled = False

    def joinChannel(self, channel):
        self.channel = channel

    def addToSchedule(self, assignID):
        self.addToScheduleCalled = True

    def removeFromScheduleByAssignID(self, assignID):
        self.removeFromScheduleByAssignIDCalled = True

    def notificationHasFadedOut(self, assignID):
        self.notificationHasFadedOutCalled = True

    def closeNotification(self, assignID):
        self.closeNotificationCalled = True