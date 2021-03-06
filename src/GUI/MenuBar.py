from PyQt5.QtWidgets import QAction, QMenuBar
from GUI.SubWindows.JoinChannelDialog import JoinChannelDialog
from GUI.SubWindows.JoinGameDialog import JoinGameDialog
from GUI.SubWindows.SettingDialog import SettingDialog

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent
        self.fileMenu = self.addMenu('&Main')
        self.setUpMainAction()
        self.fileMenu = self.addMenu('&View')
        self.fileMenu = self.addMenu('&Bot')
        self.fileMenu = self.addMenu('&Channels')
        self.setUpChannelAction()
        self.setUpChannelAction2()
        self.fileMenu = self.addMenu('&Dev')
        self.setUpDevAction()


    def setUpMainAction(self):
        loginAction = QAction('&Login', self)
        loginAction.triggered.connect(self.openLogin)
        self.fileMenu.addAction(loginAction)
        settingAction = QAction('&Settings', self)
        settingAction.triggered.connect(self.openSettings)
        self.fileMenu.addAction(settingAction)

    def openLogin(self):
        self.mainWindow.centralWidget.chatUI.chatScreen.clientIRC.openLogin()

    def openSettings(self):
        SettingDialog(self.mainWindow)

    def setUpChannelAction(self):
        joinAction = QAction('&Join Channel', self)
        joinAction.setShortcut('Ctrl+J')
        joinAction.triggered.connect(self.joinChannel)
        self.fileMenu.addAction(joinAction)

    def setUpChannelAction2(self):
        joinAction = QAction('&Join Channel by Game', self)
        joinAction.setShortcut('Ctrl+H')
        joinAction.triggered.connect(self.joinGame)
        self.fileMenu.addAction(joinAction)

    def setUpDevAction(self):
        hideMessages = QAction('&Hide Messages', self)
        hideMessages.setCheckable(True)
        hideMessages.setChecked(False)
        hideMessages.triggered.connect(self.toggleMessageButton)
        self.fileMenu.addAction(hideMessages)
        notificationTest = QAction('&Test Notification', self)
        notificationTest.setCheckable(False)
        notificationTest.setChecked(False)
        notificationTest.triggered.connect(lambda: self.mainWindow.centralWidget.chatUI.chatScreen.notificationManager.showNotification("testEvent", "testChannel", "testMessage"))
        self.fileMenu.addAction(notificationTest)

    def toggleMessageButton(self):
        self.mainWindow.centralWidget.chatUI.chatScreen.hideMessage()

    def joinChannel(self):
        JoinChannelDialog(self.mainWindow.centralWidget.chatUI)
        #self.mainWindow.centralWidget.chatUI.joinChannel()

    def joinGame(self):
        JoinGameDialog(self.mainWindow.centralWidget.chatUI)
