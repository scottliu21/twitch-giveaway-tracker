from PyQt5.QtWidgets import QDialog, QPushButton, QLabel , QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from GUI.SubWindows.LoginDialog import LoginDialog
from os import path
import requests

class GeneralLoginDialog(QDialog):
    def __init__(self, clientIRC):
        super(GeneralLoginDialog, self).__init__()
        self.loginChanged = False
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.clientIRC = clientIRC
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Login')
        position = self.clientIRC.chatScreen.chatUI.centralWidget.mainWindow.getPopUpPosition(400, 100)
        self.setGeometry(position.x(), position.y(), 400, 100)
        self.nickname = ""
        self.oauthToken = ""
        self.expire_in = 0
        self.refreshToken = ""
        self.hasLogin = False
        if path.exists("setting/login"):
            self.nickname, self.oauthToken, self.refreshToken = GeneralLoginDialog.readLoginFile()
            self.hasLogin = self.oauthToken != "" and self.nickname != "" and self.refreshToken != ""
        layout = QVBoxLayout()
        self.label = QLabel()
        changeAccountButton = QPushButton()
        changeAccountButton.setText('Change account')
        changeAccountButton.clicked.connect(self.changeAccount)
        self.connectButton = QPushButton()
        self.connectButton.setText('Connect')
        self.connectButton.clicked.connect(self.connect)
        self.updateUsername()

        buttonLayout = QHBoxLayout()
        removeLoginButton = QPushButton()
        removeLoginButton.setText("Remove login")
        removeLoginButton.clicked.connect(self.removeLogin)
        buttonLayout.addWidget(changeAccountButton)
        buttonLayout.addWidget(removeLoginButton)

        self.defaultChannelLineEdit = QLineEdit()
        try:
            defaultChannelFile = open('setting/default_channel', 'r')
            self.defaultChannelLineEdit.setText(defaultChannelFile.readline().strip())
            defaultChannelFile.close()
        except FileNotFoundError:
            self.defaultChannelLineEdit.setText("")


        layout.addWidget(self.label, 1)
        layout.addLayout(buttonLayout)
        layout.addWidget(QLabel("Default list of channels to connect to, separated by comma"))
        layout.addWidget(self.defaultChannelLineEdit)
        layout.addWidget(self.connectButton, 1)

        self.setLayout(layout)

    @staticmethod
    def refreshAccessTokenWithName(username, refreshToken):
        response = requests.post(LoginDialog.refreshTokenURL.replace("refreshToken", refreshToken))
        GeneralLoginDialog.writeLoginFile(username, response.json()["access_token"], response.json()["refresh_token"])
        return response.json()["access_token"], response.json()["refresh_token"]

    @staticmethod
    def refreshAccessTokenWithToken(refreshToken):
        username, _, _ = GeneralLoginDialog.readLoginFile()
        return GeneralLoginDialog.refreshAccessTokenWithName(username, refreshToken)

    @staticmethod
    def refreshAccessToken():
        username, _, refreshToken = GeneralLoginDialog.readLoginFile()
        return GeneralLoginDialog.refreshAccessTokenWithName(username, refreshToken)

    @staticmethod
    def getLogin():
        GeneralLoginDialog.refreshAccessToken()
        return GeneralLoginDialog.readLoginFile()

    @staticmethod
    def readLoginFile():
        file = open('setting/login', 'r')
        nickname = file.readline().strip()
        oauthToken = file.readline().strip()
        refreshToken = file.readline().strip()
        file.close()
        return nickname, oauthToken, refreshToken

    @staticmethod
    def writeLoginFile(nickname, oauthToken, refreshToken):
        file = open('setting/login', "w")
        file.write(nickname + "\n")
        file.write("oauth:" + oauthToken + "\n")
        file.write(refreshToken)
        file.close()

    @staticmethod
    def hasLoginCompleted():
        try:
            nickname, oauthToken, refreshToken = GeneralLoginDialog.readLoginFile()
            with open("setting/default_channel") as file:
                line = file.readline().strip()
        except FileNotFoundError:
            return False
        return oauthToken != "" and nickname != "" and refreshToken != "" and line != ""

    def removeLogin(self):
        open('setting/login', 'w').close()
        self.hasLogin = False
        self.nickname = None
        self.updateUsername()

    def closeEvent(self, event):
        if self.hasLoginCompleted():
            if self.loginChanged:
                self.connect()
            else:
                self.close()
        else:
            self.clientIRC.chatScreen.chatUI.centralWidget.mainWindow.close()

    def updateUsername(self):
        if not self.hasLogin:
            self.label.setText("Currently not logged in")
        else:
            self.label.setText('Currently logged in as: ' + self.nickname)
        self.connectButton.setEnabled(self.hasLogin)

    def connect(self):
        defaultChannelFile = open('setting/default_channel', 'w')
        defaultChannelFile.write(self.defaultChannelLineEdit.text())
        defaultChannelFile.close()
        self.clientIRC.nickname, self.clientIRC.password, self.clientIRC.refreshToken = GeneralLoginDialog.readLoginFile()
        self.accept()

    def loadAndUpdateLogin(self):
        self.nickname, self.oauthToken, self.refreshToken = GeneralLoginDialog.readLoginFile()
        self.hasLogin = self.hasLoginCompleted()
        self.updateUsername()

    def changeAccount(self):
        loginDialog = LoginDialog(self, self.clientIRC.chatScreen.chatUI.centralWidget.mainWindow.getPopUpPosition(300, 200), self.nickname)
        loginDialog.accepted.connect(self.loadAndUpdateLogin)
        loginDialog.exec()
