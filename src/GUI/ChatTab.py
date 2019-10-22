from GUI.UserList import UserList
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter, QHBoxLayout, QWidget
from GUI.ChannelChat import ChannelChat
import threading

class ChatTab(QWidget):
    def __init__(self, channelName, clientIRC, jsonDecoder):
        super(ChatTab, self).__init__()
        userList = UserList(self)
        self.userList = userList
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.clientIRC = clientIRC
        channelChat = ChannelChat(self, channelName, jsonDecoder)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(channelChat)
        splitter.addWidget(userList)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setHandleWidth(0)
        splitter.setStretchFactor(0, 7)
        splitter.setStretchFactor(1, 1)
        splitter.setChildrenCollapsible(False)
        layout.addWidget(splitter)
        self.jsonDecoder = jsonDecoder
        self.clientIRC.joinChannel(channelName)
        self.setLayout(layout)
        self.channelChat = channelChat
        self.channelName = '#' + channelName

    def setRoomState(self, language, emotesOnly, followersOnly, r9k, roomID, slow, subsOnly):
        self.language = language
        self.emotesOnly = emotesOnly
        self.followersOnly = followersOnly
        self.r9k = r9k
        self.roomID = roomID
        self.slow = slow
        self.subsOnly = subsOnly

