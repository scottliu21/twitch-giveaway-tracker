from PyQt5.QtCore import QThread, pyqtSignal
from queue import Queue

class ChatThread(QThread):
    newNotificationSignal = pyqtSignal()
    def __init__(self, channelChat, channelName, parent=None):
        QThread.__init__(self, parent)
        self.channelChat = channelChat
        self.messageProcessor = channelChat.messageProcessor
        self.userList = channelChat.chatTab.userList
        self.messageToBeProcessed = Queue()
        self.setObjectName(channelName)

    def processMessage(self, message):
        self.messageToBeProcessed.put(message)

    def run(self):
        message = ""
        self.channelChat.newMessageSignal.connect(lambda: self.channelChat.newMessage(message))
        while True:
            message = self.messageToBeProcessed.get()
            message = self.messageProcessor.processMessage(message, self.userList)
            self.channelChat.newMessageSignal.emit()