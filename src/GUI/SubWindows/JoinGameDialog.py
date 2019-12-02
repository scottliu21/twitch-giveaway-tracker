from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt
import re
import json
import requests

ClientID = 'm8ud9x4tqmpljbtrl5lt5vkwhk3mym'
gameName = ""
channels = {}
count = 0
checkValue = 0

headers = {'Client-ID': ClientID, }
params = (('name', gameName),)


## Gets the ID of the game you're looking for by the title of the game
## Give the function a gameName and it will return a gameID
def getGameID(gameName):
    response = requests.get('https://api.twitch.tv/helix/games', headers=headers, params=(('name', gameName),))
    games = json.loads(response.text)
    if (len(games['data']) == 0):
        gameID = -1
        return gameID
    print("Game Title: ", (games['data'][0]['name']))
    gameID = games['data'][0]['id']
    return gameID


## Lists all of the livestreams in a certain category.
## Give the function a gameID and it will return a list of all live channels and their titles.
def getListofStreams(gameID):
    response = requests.get('https://api.twitch.tv/helix/streams', headers=headers,
                            params=(('game_id', gameID), ('first', 100),))
    streamData = json.loads(response.text)
    cursor = streamData['pagination']['cursor']
    streamersList = streamData['data']
    for streamer in streamersList:
        channels[streamer['user_name']] = {'viewers': streamer['viewer_count'], 'title': streamer['title'].strip()}

    ## Loops through to get all of the channels (using pagination) until no channels remain
    while (cursor != -1):
        response = requests.get('https://api.twitch.tv/helix/streams', headers=headers,
                                params=(('game_id', gameID), ('first', 100), ('after', cursor),))
        streamData = json.loads(response.text)
        if (len(streamData['pagination']) > 0):
            cursor = streamData['pagination']['cursor']
        else:
            cursor = -1
        streamersList = streamData['data']
        for streamer in streamersList:
            channels[streamer['user_name']] = {'viewers': streamer['viewer_count'], 'title': streamer['title'].strip()}
    return channels

class JoinGameDialog(QDialog):
    def __init__(self, chatUI):
        super(JoinGameDialog, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.chatUI = chatUI
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Join Channel')
        position = self.chatUI.centralWidget.mainWindow.getPopUpPosition(300, 200)
        self.setGeometry(position.x(),position.y(), 300, 200)

        layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        self.c = QCheckBox("Only Display Streams with Giveaway in Title",self)
        self.c.stateChanged.connect(self.clickBox)
        self.c.move(40,70)
        self.c.resize(320,40)

        label = QLabel()
        label.setText('Game Name: ')
        entryBox = QLineEdit()
        joinButton = QPushButton()
        joinButton.setText('Join Channels From Game')
        joinButton.clicked.connect(self.joinChannelMessage)
        cancelButton = QPushButton()
        cancelButton.setText('Cancel')
        cancelButton.clicked.connect(self.close)

        layout2.addWidget(label, 1)
        layout2.addWidget(entryBox, 5)
        layout3.addWidget(joinButton, 4)
        layout3.addWidget(cancelButton, 2)

        layout.addLayout(layout2)
        layout.addLayout(layout3)
        self.entryBox = entryBox
        self.setLayout(layout)
        self.exec()

    #Determines if the box is checked
    def clickBox(self, state):
        global checkValue
        if state == QtCore.Qt.Checked:
            checkValue = 1
            print(checkValue)
        else:
            checkValue = 0
            print(checkValue)

    def joinChannelMessage(self):
        message = self.entryBox.text().lower().strip()
        if message is not '':
            #Gets the game ID, returns -1 if the user input an invalid title.
            gameID = getGameID(message)
            if gameID == -1:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error: Invalid game name")
                msg.setInformativeText("Game name must match a category on Twitch")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                self.close()
            else:

                channels = getListofStreams(gameID)
                if checkValue == 0:
                    for x in list(channels.keys())[:3]:
                        self.chatUI.chatScreen.joinChannel(x.lower())
                if checkValue == 1:
                    searchResults = []
                    for x in channels:
                        if re.search("[Gg][Ii][Vv]", channels[x]['title']):
                            searchResults.append(x)
                    for x in searchResults[:3]:
                        self.chatUI.chatScreen.joinChannel(x.lower())
        self.close()