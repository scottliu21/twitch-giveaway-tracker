from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QGroupBox, QGridLayout, QFontDialog
from PyQt5.QtGui import QFont
from Util.SettingManager import SettingManager

class MainWidget(QWidget):
    def __init__(self, settingDialog):
        super(MainWidget, self).__init__(settingDialog)
        self.settingDialog = settingDialog
        layout = QVBoxLayout()

        settings = SettingManager.getSettingFileContent(SettingManager.MAIN_SETTING_FILE)
        chatFontGroupBox = QGroupBox(self)
        chatFontGroupBox.setTitle("Chat Font")
        chatFontLayout = QGridLayout()
        chatFontLayout.addWidget(QLabel("Font Name:"), 0, 0)
        self.chatFont = QLineEdit()
        self.chatFont.setText(settings[0])
        self.chatFont.setEnabled(False)
        chatFontLayout.setContentsMargins(5, 5, 5, 5)
        chatFontLayout.addWidget(self.chatFont, 0, 1)
        selectFontButton = QPushButton("Select Font")
        selectFontButton.clicked.connect(self.chooseFont)
        chatFontLayout.addWidget(selectFontButton, 1, 2)
        chatFontLayout.addWidget(QLabel("Font Size:"), 1, 0)
        self.chatFontSize = QLineEdit()
        self.chatFontSize.setText(settings[1])
        self.chatFontSize.setEnabled(False)
        chatFontLayout.addWidget(self.chatFontSize, 1, 1)
        chatFontLayout.addWidget(QLabel("Line Spacing:"), 2, 0)
        self.chatLineSpacing = QLineEdit()
        self.chatLineSpacing.setText(settings[2])
        self.chatLineSpacing.setEnabled(False)
        chatFontLayout.addWidget(self.chatLineSpacing, 2, 1)
        chatFontGroupBox.setLayout(chatFontLayout)
        layout.addWidget(chatFontGroupBox)

        self.setLayout(layout)

    def chooseFont(self):
        fontDialog = QFontDialog()
        fontDialog.setCurrentFont(QFont(self.chatFont.text(), int(self.chatFontSize.text()), -1, False))
        fontDialog.exec()
        self.chatFont.setText(fontDialog.currentFont().family())
        self.chatFontSize.setText(str(int(fontDialog.currentFont().pointSizeF())))

    def saveSetting(self):
        settings = []
        settings.append(self.chatFont.text())
        settings.append(self.chatFontSize.text())
        settings.append(self.chatLineSpacing.text())
        SettingManager.saveSetting(SettingManager.MAIN_SETTING_FILE, settings)