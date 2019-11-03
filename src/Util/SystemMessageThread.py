import threading
from queue import Queue

class SystemMessageThread(threading.Thread):
    def __init__(self, parent, chatScreen):
        super().__init__(target=self.run, args=('',))
        self.systemMessageProcessor = parent
        self.chatScreen = chatScreen
        self.messageToBeProcessed = Queue()
        self.daemon = True
        self.enabled = True
        self.setName('SystemMesageThread')

    def stopThread(self):
        self.enabled = False

    def newMessage(self, message):
        self.messageToBeProcessed.put(message)

    def run(self):
        while self.enabled:
            message = self.messageToBeProcessed.get()
            self.systemMessageProcessor.processMessage(message)

