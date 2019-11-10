from PyQt5.QtWidgets import QDialog, QPushButton, QLabel , QVBoxLayout, QApplication, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
import time
import math

class NotificationDialog(QDialog):
    NOTIFICATION_LIVETIME = 2000
    def __init__(self, assignID, eventDescription, channelName, message, positionNumber, font, notificationManager):
        super(NotificationDialog, self).__init__(notificationManager.chatScreen.chatUI.centralWidget.mainWindow)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.assignID = assignID
        self.mainWindow = notificationManager.chatScreen.chatUI.centralWidget.mainWindow
        self.notificationManager = notificationManager
        self.eventDescription = eventDescription
        self.channelName = channelName
        self.message = message
        self.closeTime = time.time() + NotificationDialog.NOTIFICATION_LIVETIME
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.right = QApplication.desktop().screenGeometry().bottomRight().x() + 1
        self.bottom = QApplication.desktop().screenGeometry().bottomRight().y()
        self.height = math.floor(QApplication.desktop().screenGeometry().bottomRight().y() / 10)
        self.width = math.floor(QApplication.desktop().screenGeometry().bottomRight().x() / 6)
        self.setGeometry(self.right - self.width, self.height * positionNumber, self.width, self.height - 10)
        print(self.assignID, self.right - self.width, self.height * positionNumber, self.width, self.height * (positionNumber + 1) - 10)
        print(self.assignID, self.geometry())

        label = QLabel()
        label.setObjectName("NotificationLabel")
        label.setText("\t" + eventDescription + "\n\t" + channelName + "\n\t" + message)
        label.setFont(font)
        label.mouseReleaseEvent = self.clicked
        label.setMouseTracking(True)
        label.leaveEvent = self.mouseLeave
        label.enterEvent = self.mouseEnter

        layout1 = QVBoxLayout()
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.addWidget(label)
        self.setLayout(layout1)
        self.setWindowModality(Qt.NonModal)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setEasingCurve(QEasingCurve.InCubic)
        self.animation.setDuration(1000)
        self.animation.setStartValue(self.windowOpacity())
        self.animation.setEndValue(0.1)
        self.hovered = True
        self.animation.finished.connect(self.fadeOutClose)
        self.show()

    def moveUpByOne(self):
        self.setGeometry(self.x(), self.y() - self.height, self.width, self.height - 10)

    def mouseLeave(self, _):
        self.closeTime = time.time() + NotificationDialog.NOTIFICATION_LIVETIME
        self.notificationManager.addToSchedule(self)

    def mouseEnter(self, _):
        self.animation.stop()
        self.setWindowOpacity(1.0)
        self.notificationManager.removeFromScheduleByAssignID(self.assignID)

    def fadeOutClose(self):
        self.notificationManager.notificationHasFadedOut(self.assignID)
        self.close()

    def fadeOut(self):
        self.animation.start()

    def clicked(self, event):
        if event.button() == Qt.RightButton:
            self.mainWindow.centralWidget.chatUI.chatScreen.joinChannel(self.channelName)
        self.notificationManager.closeNotification(self.assignID)
        self.close()

    def __eq__(self, other):
        return self.assignID == other