from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtCore import Qt
import random
from GUI.Chat.User import  UserListEntry
import time


class WhisperChat(QTextBrowser):
    def __init__(self, chatScreen, whisperer, clientIRC):
        super(WhisperChat, self).__init__(chatScreen)
        self.chatScreen = chatScreen
        self.clientIRC = clientIRC
        self.scrollToBottom = True
        self.lastSent = ''
        self.setReadOnly(True)
        self.anchorClicked.connect(self.checkClick)
        self.setAcceptRichText(True)
        self.setOpenLinks(False)
        self.verticalScrollBar().rangeChanged.connect(self.scrollBar)
        self.verticalScrollBar().sliderReleased.connect(self.shouldKeepScrolling)
        self.channelName = '$' + whisperer
        #add wheel event

    def setUpWhisperChat(self):
        self.userColor = random.choice(UserListEntry.DEFAULT_COLOR)

    def checkClick(self, link):
        print(link.toString())

    def newMessage(self, message):
        self.append(message)

    def newSentMessage(self, message):
        finalMessage = '<font color="#00BFFF">[' + time.strftime('%H:%M:%S') + ']</font>'\
                       + '<a href="' + self.clientIRC.nickname + '" style="text-decoration:none" '\
                       + 'style="color:' + self.clientIRC.userColor + '">'\
                       + '<b>' + self.clientIRC.userDisplayName + ': </b></a>'\
                       +'<font color="#00BFFF">[' + message + ']</font>'
        #add emotes later
        self.append(finalMessage)

    def shouldKeepScrolling(self):
        if self.verticalScrollBar().value() == self.verticalScrollBar().maximum():
            self.scrollToBottom = True
        else:
            self.scrollToBottom = False

    def scrollBar(self):
        if self.scrollToBottom:
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())