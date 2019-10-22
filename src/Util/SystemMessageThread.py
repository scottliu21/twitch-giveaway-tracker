import threading
from queue import Queue

class SystemMessageThread(threading.Thread):
    def __init__(self, parent, chatScreen):
        super().__init__(target=self.run, args=('',))
        self.systemMessageProcessor = parent
        self.chatScreen = chatScreen
        self.messageToBeProcessed = Queue()
        self.daemon = True
        self.setName('SystemMesageThread')

    def newMessage(self, message):
        self.messageToBeProcessed.put(message)

    def run(self):
        while True:
            message = self.messageToBeProcessed.get()
            self.systemMessageProcessor.processMessage(message)

