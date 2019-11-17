from Util.MessageProcessor import MessageProcessor
from GUI.Chat.ChatThread import ChatThread
from PyQt5.QtWidgets import QTextBrowser
from Util.SettingManager import SettingManager

class ChannelChat(QTextBrowser):
    def __init__(self, chatTab, channelName, jsonDecoder):
        super(ChannelChat, self).__init__(chatTab)
        self.chatTab = chatTab
        self.messageProcessor = MessageProcessor(jsonDecoder, self.chatTab.clientIRC.chatScreen.font.pointSizeF() / 12 * 16)
        self.chatThread = ChatThread(self, channelName)
        self.channelName = channelName
        self.chatThread.start()
        self.setReadOnly(True)
        self.anchorClicked.connect(self.checkClick)
        self.setAcceptRichText(True)
        self.setOpenLinks(False)
        self.scrollToBottom = True
        self.lastSent = ''
        self.verticalScrollBar().rangeChanged.connect(self.scrollBar)
        self.verticalScrollBar().sliderReleased.connect(self.shouldKeepScrolling)
        self.verticalScrollBar().valueChanged.connect(self.shouldKeepScrolling)
        self.setFont(self.chatTab.clientIRC.chatScreen.font)
        self.document().setDefaultStyleSheet("background-color: yellow")
        self.setStyleSheet(SettingManager.getHTMLSettingContent(SettingManager.CHAT_CSS_FILE))
        #add wheel event

    def closeChat(self):
        self.chatThread.stopThread()
        self.chatThread.messageToBeProcessed.put("")
        self.chatThread.join()

    def checkClick(self, link):
        print(link.toString())

    def newMessage(self, message):
        #self.textCursor().insertHtml(message)
        self.append(message)

    def shouldKeepScrolling(self):
        if self.verticalScrollBar().value() == self.verticalScrollBar().maximum():
            self.scrollToBottom = True
        else:
            self.scrollToBottom = False

    def scrollBar(self):
        if self.scrollToBottom:
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
