from PyQt5.QtWidgets import QDialog, QPushButton, QLabel , QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.Qt import QApplication
from Util.SettingManager import  SettingManager
import webbrowser
import urllib.parse
import http.server
import requests


class LoginDialog(QDialog):
    authorizationTokenURL = "https://api.twitch.tv/kraken/oauth2/authorize?client_id=w07tun6ja438fsymn61ei88tm8kw7q&redirect_uri=http://127.0.0.1:60202&response_type=code&force_verify=true&scope=chat:edit+chat:read+whispers:read+whispers:edit+user_subscriptions+user_follows_edit+user_blocks_edit&claims={\"id_token\":{\"email_verified\":null}}'"
    oauthTokenURL = "https://id.twitch.tv/oauth2/token?client_id=w07tun6ja438fsymn61ei88tm8kw7q&client_secret=8k0lki8kgnimfoq76x39xtp2e890a8&code=REPLACE&grant_type=authorization_code&redirect_uri=http://127.0.0.1:60202"
    VALIDATE_URL = "https://id.twitch.tv/oauth2/validate"
    refreshTokenURL = "https://id.twitch.tv/oauth2/token?grant_type=refresh_token&refresh_token=refreshToken&client_id=w07tun6ja438fsymn61ei88tm8kw7q&client_secret=8k0lki8kgnimfoq76x39xtp2e890a8"

    def __init__(self, parent, position, nickname):
        super(LoginDialog, self).__init__()
        self.loginChanged = False
        self.generalLoginDialog = parent
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Login Configuration')
        self.serverThread = None
        self.setGeometry(position.x(), position.y(), 300, 200)
        self.nickname = nickname
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.hasLogin = self.nickname
        self.updateUsername()
        loginButton = QPushButton()
        loginButton.setText('Create new login with default browser')
        loginButton.clicked.connect(self.getOauthTokenWithBrowser)
        loginLinkButton = QPushButton()
        loginLinkButton.setText('Copy link to clipboard')
        loginLinkButton.clicked.connect(self.getOauthTokenWithCopiedLink)
        closeButton = QPushButton()
        closeButton.setText('Close')
        closeButton.clicked.connect(self.close)

        layout.addWidget(self.label, 1)
        layout.addWidget(loginButton, 1)
        layout.addWidget(loginLinkButton, 1)
        layout.addWidget(closeButton, 1)

        self.setLayout(layout)

    def updateUsername(self):
        if not self.hasLogin:
            self.label.setText("Currently not logged in")
        else:
            self.label.setText('Currently logged in as\n\n' + self.nickname)

    def getOauthTokenWithBrowser(self):
        webbrowser.open(self.authorizationTokenURL)
        self.getOauthToken()

    def getOauthToken(self):
        if not self.serverThread:
            self.serverThread = ServerQThread(self)
            self.serverThread.connectSignals(self.requestAccepted)
            self.serverThread.start()

    def requestAccepted(self, token):
        self.loginChanged = True
        self.hasLogin = True
        response = requests.post(self.oauthTokenURL.replace("REPLACE", token))
        oauthToken = response.json()['access_token']
        refreshToken = response.json()['refresh_token']
        response = requests.get(self.VALIDATE_URL, headers={"Authorization": "OAuth " + oauthToken})
        self.nickname = response.json()['login']
        SettingManager.saveSetting(SettingManager.LOGIN_FILE, [self.nickname, "oauth:" + oauthToken, refreshToken])
        self.updateUsername()

    def closeEvent(self, event):
        if self.serverThread:
            self.serverThread.shutDown()
            self.serverThread.terminate()
            self.serverThread.wait()
        if self.loginChanged:
            self.accept()
        else:
            self.reject()

    def getOauthTokenWithCopiedLink(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.authorizationTokenURL)
        clipboard.text()
        self.getOauthToken()

class ServerQThread(QThread):
    acceptedSignal = pyqtSignal()
    instance = None

    def connectSignals(self, acceptedMethod):
        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 60202), Handler)
        ServerQThread.instance = self
        self.acceptedSignal.connect(lambda: acceptedMethod(self.server.token))

    def run(self):
        self.server.serve_forever()

    def shutDown(self):
        self.server.shutdown()
        self.wait()


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.requestline)[3])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if 'code' not in query:
            self.wfile.write(self._html("Close this page and log in again"))
        else:
            self.server.token = query["code"][0]
            self.wfile.write(self._html("You can close this page now"))
            ServerQThread.instance.acceptedSignal.emit()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!