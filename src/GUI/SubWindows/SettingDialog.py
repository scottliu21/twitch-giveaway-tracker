from PyQt5.QtWidgets import QDialog, QHBoxLayout, QStackedLayout, QListWidget, QWidget
from PyQt5.QtCore import Qt
from GUI.SubWindows.SettingPages.ColorsWidget import ColorsWidget
from GUI.SubWindows.SettingPages.MainWidget import MainWidget
from GUI.SubWindows.SettingPages.NotificationWidget import  NotificationWidget

class SettingDialog(QDialog):
    def __init__(self, mainWindow):
        super(SettingDialog, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.mainWindow = mainWindow
        self.setWindowTitle('Settings')
        position = self.mainWindow.getPopUpPosition(600, 510)
        self.setGeometry(position.x(), position.y(), 600, 510)
        self.setFixedHeight(510)
        self.setFixedWidth(600)
        layout = QHBoxLayout()
        layout.setContentsMargins(5,5,5,5)
        self.settingList = QListWidget()
        layout.addWidget(self.settingList, 1)
        settingContent = QWidget(self)
        self.layout = QStackedLayout()
        settingContent.setLayout(self.layout)
        self.setUpPages()
        self.settingList.itemSelectionChanged.connect(self.switchSettingPage)

        layout.addWidget(settingContent, 9)
        self.setLayout(layout)
        self.exec()

    def setUpPages(self):
        self.settingList.addItem("Main")
        self.layout.addWidget(MainWidget(self))
        self.settingList.addItem("Colors")
        self.layout.addWidget(ColorsWidget(self))
        self.settingList.addItem("Macros")
        self.settingList.addItem("OBS")
        self.settingList.addItem("Notification")
        self.layout.addWidget(NotificationWidget(self))


    def switchSettingPage(self):
        self.layout.setCurrentIndex(self.settingList.currentRow())

    def closeEvent(self, event):
        for i in range(self.layout.count()-1, -1, -1):
            self.layout.widget(i).saveSetting()
        event.accept()