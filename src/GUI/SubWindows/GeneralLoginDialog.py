from PyQt5.QtWidgets import QDialog, QPushButton, QLabel , QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from GUI.SubWindows.LoginDialog import LoginDialog
from Util.SettingManager import SettingManager
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
        self.hasLogin = SettingManager.checkLoginFilesAreCompleted()
        if self.hasLogin:
            [self.nickname, self.oauthToken, self.refreshToken] = SettingManager.getSettingFileContent(SettingManager.LOGIN_FILE)
        layout = QVBoxLayout()
        self.label = QLabel()
        changeAccountButton = QPushButton()
        changeAccountButton.setText('Change account')
        changeAccountButton.clicked.connect(self.changeAccount)
        self.connectButton = QPushButton()
        self.connectButton.setText('Connect')
        self.connectButton.clicked.connect(self.connect)

        buttonLayout = QHBoxLayout()
        removeLoginButton = QPushButton()
        removeLoginButton.setText("Remove login")
        removeLoginButton.clicked.connect(self.removeLogin)
        buttonLayout.addWidget(changeAccountButton)
        buttonLayout.addWidget(removeLoginButton)

        self.defaultChannelLineEdit = QLineEdit()
        if self.hasLogin:
            self.defaultChannelLineEdit.setText(SettingManager.getSettingFileContent(SettingManager.DEFAULT_CHANNEL_FILE)[0])
        else:
            self.defaultChannelLineEdit.setText("")
        self.defaultChannelLineEdit.returnPressed.connect(self.connect)
        self.defaultChannelLineEdit.textChanged[str].connect(self.enableConnectButton)

        layout.addWidget(self.label, 1)
        layout.addLayout(buttonLayout)
        layout.addWidget(QLabel("Default list of channels to connect to, separated by comma"))
        layout.addWidget(self.defaultChannelLineEdit)
        layout.addWidget(self.connectButton, 1)

        self.setLayout(layout)
        self.updateUsername()

    @staticmethod
    def refreshAccessTokenWithName(username, refreshToken):
        response = requests.post(LoginDialog.refreshTokenURL.replace("refreshToken", refreshToken))
        return [username, response.json()["access_token"], response.json()["refresh_token"]]

    @staticmethod
    def refreshAccessTokenWithToken(refreshToken):
        [username, _, _] = SettingManager.getSettingFileContent(SettingManager.LOGIN_FILE)
        return GeneralLoginDialog.refreshAccessTokenWithName(username, refreshToken)

    @staticmethod
    def refreshAccessToken():
        [username, _, refreshToken] = SettingManager.getSettingFileContent(SettingManager.LOGIN_FILE)
        return GeneralLoginDialog.refreshAccessTokenWithName(username, refreshToken)

    @staticmethod
    def reFreshTokenAndGetLogin():
        response = GeneralLoginDialog.refreshAccessToken()
        if response:
            GeneralLoginDialog.writeLoginFile(response[0], response[1], response[2])
        else:
            return None
        return SettingManager.getSettingFileContent(SettingManager.LOGIN_FILE)

    @staticmethod
    def writeLoginFile(nickname, oauthToken, refreshToken):
        content = []
        content.append(nickname)
        content.append("oauth:" + oauthToken)
        content.append(refreshToken)
        SettingManager.saveSetting(SettingManager.LOGIN_FILE, content)

    def removeLogin(self):
        SettingManager.clearSettingFile(SettingManager.LOGIN_FILE)
        self.hasLogin = False
        self.updateUsername()

    def enableConnectButton(self):
        self.connectButton.setEnabled(not self.defaultChannelLineEdit.text().strip() == '' and self.hasLogin)

    def closeEvent(self, event):
        if SettingManager.checkLoginFilesAreCompleted():
            if self.loginChanged:
                self.connect()
            else:
                self.close()
        else:
            self.clientIRC.chatScreen.chatUI.centralWidget.mainWindow.close()

    def updateUsername(self):
        if self.nickname == '' or not self.hasLogin:
            self.label.setText("Currently not logged in")
        else:
            self.label.setText('Currently logged in as: ' + self.nickname)
        self.enableConnectButton()

    def connect(self):
        SettingManager.saveSetting(SettingManager.DEFAULT_CHANNEL_FILE, [self.defaultChannelLineEdit.text()])
        self.accept()

    def loadAndUpdateLogin(self):
        [self.nickname, self.oauthToken, self.refreshToken] = SettingManager.getSettingFileContent(SettingManager.LOGIN_FILE)
        self.hasLogin = True
        self.updateUsername()

    def changeAccount(self):
        loginDialog = LoginDialog(self, self.clientIRC.chatScreen.chatUI.centralWidget.mainWindow.getPopUpPosition(300, 200), self.nickname)
        loginDialog.accepted.connect(self.loadAndUpdateLogin)
        loginDialog.exec()
