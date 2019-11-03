from PyQt5.QtWidgets import QDialog, QPushButton, QLabel , QVBoxLayout
from PyQt5.QtCore import Qt
import webbrowser
import urllib.parse
import http.server
import requests
from os import path


class LoginDialog(QDialog):
    authorizationTokenURL = "https://api.twitch.tv/kraken/oauth2/authorize?client_id=w07tun6ja438fsymn61ei88tm8kw7q&redirect_uri=http://127.0.0.1:60202&response_type=code&force_verify=true&scope=chat:edit+chat:read+whispers:read+whispers:edit+user_subscriptions+user_follows_edit+user_blocks_edit&claims={\"id_token\":{\"email_verified\":null}}'"
    oauthTokenURL = "https://id.twitch.tv/oauth2/token?client_id=w07tun6ja438fsymn61ei88tm8kw7q&client_secret=8k0lki8kgnimfoq76x39xtp2e890a8&code=REPLACE&grant_type=authorization_code&redirect_uri=http://127.0.0.1:60202"
    server = ""
    VALIDATE_URL = "https://id.twitch.tv/oauth2/validate"
    refreshTokenURL = "https://id.twitch.tv/oauth2/token?grant_type=refresh_token&refresh_token=refreshToken&client_id=w07tun6ja438fsymn61ei88tm8kw7q&client_secret=8k0lki8kgnimfoq76x39xtp2e890a8"
    def __init__(self, clientIRC):
        super(LoginDialog, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.clientIRC = clientIRC
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Login')
        position = self.clientIRC.chatScreen.chatUI.centralWidget.mainWindow.getPopUpPosition(300, 200)
        self.setGeometry(position.x(),position.y(), 300, 200)
        self.nickname = ""
        self.oauthToken = ""
        self.expire_in = 0
        self.refreshToken = ""
        self.hasLogin = False
        if path.exists("setting/login"):
            self.nickname, self.oauthToken, self.refreshToken = LoginDialog.readLoginFile()
            self.hasLogin = self.oauthToken != "" and self.nickname != "" and self.refreshToken != ""

        layout = QVBoxLayout()
        self.label = QLabel()
        self.updateUsername()
        loginButton = QPushButton()
        loginButton.setText('Create new login with default browser')
        loginButton.clicked.connect(self.getOauthTokenWithBrowser)
        # loginLinkButton = QPushButton()
        # loginLinkButton.setText('Copy link to clipboard')
        # loginLinkButton.clicked.connect(self.getOauthTokenWithCopiedLink)
        self.connectButton = QPushButton()
        self.connectButton.setText('Connect')
        self.connectButton.clicked.connect(self.connect)
        self.connectButton.setEnabled(self.hasLogin)

        layout.addWidget(self.label, 1)
        layout.addWidget(loginButton, 1)
        # layout.addWidget(loginLinkButton, 1)
        layout.addWidget(self.connectButton, 1)

        self.setLayout(layout)
        self.exec()



    @staticmethod
    def refreshAccessTokenWithName(username, refreshToken):
        response = requests.post(LoginDialog.refreshTokenURL.replace("refreshToken", refreshToken))
        LoginDialog.writeLoginFile(username, response.json()["access_token"], response.json()["refresh_token"])
        return response.json()["access_token"], response.json()["refresh_token"]

    @staticmethod
    def refreshAccessTokenWithToken(refreshToken):
        username, _, _ = LoginDialog.readLoginFile()
        return LoginDialog.refreshAccessTokenWithName(username, refreshToken)

    @staticmethod
    def refreshAccessToken():
        username, _, refreshToken = LoginDialog.readLoginFile()
        return LoginDialog.refreshAccessTokenWithName(username, refreshToken)

    @staticmethod
    def getLogin():
        LoginDialog.refreshAccessToken()
        return LoginDialog.readLoginFile()

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
        try :
            nickname, oauthToken, refreshToken = LoginDialog.readLoginFile()
        except FileNotFoundError:
            return False
        return oauthToken != "" and nickname != "" and refreshToken != ""

    def updateUsername(self):
        if not self.hasLogin:
            self.label.setText("Currently not logged in")
        else:
            self.label.setText('Currently logged in as: ' + self.nickname)

    def connect(self):
        self.clientIRC.nickname, self.clientIRC.password, self.clientIRC.refreshToken = LoginDialog.readLoginFile()
        self.close()

    def getOauthTokenWithBrowser(self):
        webbrowser.open(self.authorizationTokenURL)
        self.getOauthToken()

    def getOauthToken(self):
        self.server = http.server.HTTPServer(("127.0.0.1", 60202), Handler)
        self.server.success = False
        self.server.handle_request()

        if self.server.success:
            response = requests.post(self.oauthTokenURL.replace("REPLACE", self.server.token))
            self.oauthToken = response.json()['access_token']
            self.refreshToken = response.json()['refresh_token']
            response = requests.get(self.VALIDATE_URL, headers={"Authorization": "OAuth " + self.oauthToken})
            self.nickname = response.json()['login']
            self.hasLogin = True
            LoginDialog.writeLoginFile(self.nickname, self.oauthToken, self.refreshToken)
            self.connectButton.setEnabled(True)
            self.updateUsername()
        else:
            self.hasLogin = False
            self.connectButton.setDisabled(True)
            self.updateUsername()
        self.server.server_close()


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.requestline)[3])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if 'code' not in query:
            self.wfile.write(self._html("Close this page and log in again"))
            self.server.success = False
        else:
            self.server.token = query["code"][0]
            self.server.success = True
            self.wfile.write(self._html("You can close this page now"))

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!