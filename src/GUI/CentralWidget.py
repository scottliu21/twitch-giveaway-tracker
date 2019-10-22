from PyQt5.QtWidgets import QWidget, QVBoxLayout
from GUI.EntryBox import EntryBox
from GUI.ChatUI import ChatUI

class CentralWidget(QWidget):
    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)
        self.mainWindow = parent
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        chatUI = ChatUI(self)
        self.chatUI = chatUI
        layout.addWidget(chatUI)
        entryBox = EntryBox(self, chatUI.chatScreen)
        layout.addWidget(entryBox)

    def newMessage(self, channelName, messageType, user, message):
        self.chatUI.chat.newMessage(channelName, messageType, user, message)
