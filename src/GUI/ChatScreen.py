import re
from PyQt5.QtWidgets import QShortcut, QTabWidget
from PyQt5.QtGui import QKeySequence, QFont
from Util.ClientIRC import ClientIRC
from GUI.ChatTab import ChatTab
from Util.JSONDecoder import JSONDecoder
from GUI.WhisperChat import WhisperChat
from PyQt5.QtCore import pyqtSignal

class ChatScreen(QTabWidget):
    newWhisperSignal = pyqtSignal(str)
    WHISPER = re.compile('(\d\d:\d\d:\d\d) .*color=([^;]*);display-name=(([^A-Za-z]+)|([^;]+));emotes=([^;]*);.*:([^!]+).*WHISPER.*:(.*)')
    def __init__(self, parent):
        super(ChatScreen, self).__init__(parent)
        self.showMessage = True
        file = open('setting/MainSetting', 'r')
        self.font = QFont(file.readline()[:-1], int(file.readline()[:-1]), -1, False)
        file.close()
        self.jsonDecoder = JSONDecoder()
        self.tabs = {}
        self.clientIRC = ClientIRC(self)
        self.clientIRC.start()
        self.setAutoFillBackground(True)
        default_channel = open('setting/default_channel', 'r')
        for line in default_channel:
            self.joinChannel(line.replace('\n', ''))
        default_channel.close()
        QShortcut(QKeySequence('Ctrl+Tab'), self, self.nextTab)
        QShortcut(QKeySequence('Ctrl+W'), self, self.closeTab)
        self.newWhisperSignal.connect(self.newWhisper)

    def joinChannel(self, channelName):
        chatTab = self.tabs.get('#' + channelName, None)
        if chatTab is None:
            chatTab = ChatTab(channelName, self.clientIRC, self.jsonDecoder)
            self.tabs['#' + channelName] = chatTab
            self.setCurrentIndex(self.addTab(chatTab, '#' + channelName))
            chatTab.channelChat.setUpdatesEnabled(self.showMessage)
        else:
            index = 0
            for index in range(0, self.count()):
                if self.widget(index).channelName == '#' + channelName:
                    break
            self.setCurrentIndex(index)

    def newMessage(self, channelName, message):
        chatTab = self.tabs.get(channelName, None)
        chatTab.channelChat.chatThread.processMessage(message)

    def hideMessage(self):
        self.showMessage = not self.showMessage
        for chatTab in self.tabs:
            self.tabs.get(chatTab).channelChat.setUpdatesEnabled(self.showMessage)

    def nextTab(self):
        if self.currentIndex() == self.count() - 1:
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(self.currentIndex() + 1)

    def closeTab(self):
        if self.count() > 1:
            if '#' in self.widget(self.currentIndex()).channelName:
                self.clientIRC.leaveChannel(self.widget(self.currentIndex()).channelName)
            self.tabs.pop(self.widget(self.currentIndex()).channelName)
            if self.currentIndex() + 1 == self.count():
                self.setCurrentIndex(self.count() - 2)
                self.widget(self.count() - 1).close()
                self.removeTab(self.count() - 1)
            else:
                self.setCurrentIndex(self.currentIndex() + 1)
                self.widget(self.currentIndex() - 1).close()
                self.removeTab(self.currentIndex() - 1)

    def newWhisperChat(self, nick):
        whisperChat = WhisperChat(self, nick, self.clientIRC)
        whisperChat.setUpWhisperChat()
        self.addTab(whisperChat, '$' + nick)
        self.tabs['$' + nick] = whisperChat
        return whisperChat

    def newWhisper(self, message):
        result = re.search(ChatScreen.WHISPER, message)
        whisperChat = self.tabs.get('$' + result.group(7), None)
        if whisperChat is None:
            whisperChat = self.newWhisperChat(result.group(7))
        finalMessage = '[' + result.group(1) + '] <a href="' + result.group(7) + '" style="text-decoration:none" '
        if result.group(2):
            finalMessage += 'style="color:' + result.group(2) + '">'
        else:
            finalMessage += 'style="color:' + whisperChat.userColor + '">'
        if result.group(3) is not None:
            if result.group(4) is not None:
                displayName = result.group(4) + ' (' + result.group(7) + ')'
            else:
                displayName = result.group(5)
        else:
            displayName = result.group(7)
        #add emotes later
        finalMessage += '<b>' + displayName + ': </b></a>' + result.group(8)
        whisperChat.newMessage(finalMessage)
