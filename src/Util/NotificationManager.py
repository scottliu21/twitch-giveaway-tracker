from GUI.SubWindows.NotificationDialog import NotificationDialog
from PyQt5.QtCore import QTimer
from PyQt5.Qt import QSound, QFont
import time


class NotificationManager:
    def __init__(self, chatScreen):
        self.notifications = []
        self.schedule = []
        self.chatScreen = chatScreen
        self.assignID = 0
        self.isTimerRunning = False
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.notificationExpiresFadeout)
        self.updateSetting()


    def removeFromScheduleByAssignID(self, assignID):
        index = self.schedule.index(assignID)
        self.schedule.pop(index)
        if index == 0:
            self.getNewTimerJob()

    def addToSchedule(self, notificationDialog):
        self.schedule.append(notificationDialog)
        print(self.schedule[0])
        if not self.isTimerRunning:
            self.getNewTimerJob()

    def removeFromNotificationWithAssignID(self, assignID):
        self.notifications.pop(self.notifications.index(assignID))

    def getNewTimerJob(self):
        self.timer.stop()
        if len(self.schedule) > 0:
            self.isTimerRunning = True
            self.timer.setInterval(self.schedule[0].closeTime - time.time())
            self.timer.start()
        else:
            self.isTimerRunning = False

    def moveNotificationsUp(self, index):
        for i in range(index, len(self.notifications)):
            self.notifications[i].moveUpByOne()

    def updateSetting(self):
        file = open('setting/NotificationSetting', 'r')
        self.font = QFont(file.readline().strip(), int(file.readline().strip()), -1, False)
        self.chatScreen.chatUI.centralWidget.mainWindow.setStyleSheet("QLabel#NotificationLabel { background-color : " + file.readline().strip() +  "; color : " + file.readline().strip() + "; }")
        self.qSound = QSound(file.readline().strip())
        file.close()

    def closeNotification(self, assignID):
        index = self.notifications.index(assignID)
        self.removeFromNotificationWithAssignID(assignID)
        self.moveNotificationsUp(index)

    def notificationExpiresFadeout(self):
        self.schedule[0].fadeOut()

    def notificationHasFadedOut(self, assignID):
        self.schedule.pop(0)
        index = self.notifications.index(assignID)
        self.notifications.pop(index)
        self.moveNotificationsUp(index)
        self.getNewTimerJob()

    # eventDescription = what's this highlight for, Raffle Detected? Username Mentioned? User Won Raffle?
    # channelName = the name of the channel this highlight happens in
    # message = the message, i.e. the giveaway starting message from bot, the winner message, the message the user is mentioned in etc, give only the message part in raw irc
    def showNotification(self, eventDescription, channelName, message):
        notificationDialog = NotificationDialog(self.assignID, eventDescription, channelName, message, len(self.notifications), self.font, self)
        self.assignID = self.assignID + 1
        self.notifications.append(notificationDialog)
        self.addToSchedule(notificationDialog)
        self.qSound.play()


