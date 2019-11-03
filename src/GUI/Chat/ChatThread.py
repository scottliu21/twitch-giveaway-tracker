import threading
from queue import Queue

class ChatThread(threading.Thread):
    def __init__(self, channelChat, channelName):
        super().__init__(target=self.run, args=('',))
        self.channelChat = channelChat
        self.messageProcessor = channelChat.messageProcessor
        self.userList = channelChat.chatTab.userList
        self.daemon = True
        self.enabled = True
        self.messageToBeProcessed = Queue()
        self.setName(channelName + 'MessageProcessorThread')

    def stopThread(self):
        self.enabled = False

    def processMessage(self, message):
        self.messageToBeProcessed.put(message)

    def run(self):
        while self.enabled:
            message = self.messageToBeProcessed.get()
            self.messageProcessor.processMessage(message, self.channelChat, self.userList)