from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QFontDialog, QColorDialog, QFileDialog
from PyQt5.Qt import QSound, QColor
from PyQt5.QtGui import QFont
from Util.SettingManager import SettingManager
import os

class NotificationWidget(QWidget):
    def __init__(self, settingDialog):
        super(NotificationWidget, self).__init__(settingDialog)
        self.settingDialog = settingDialog
        layout = QVBoxLayout()

        settings = SettingManager.getSettingFileContent(SettingManager.NOTIFICATION_SETTING_FILE)
        notificationFontGroupBox = QGroupBox(self)
        notificationFontGroupBox.setTitle("Notification Style")
        notificationStyleLayout = QGridLayout()
        notificationStyleLayout.addWidget(QLabel("Font Name:"), 0, 0)
        self.notificationFont = QLineEdit()
        self.notificationFont.setText(settings[0])
        self.notificationFont.setEnabled(False)
        notificationStyleLayout.setContentsMargins(5, 5, 5, 5)
        notificationStyleLayout.addWidget(self.notificationFont, 0, 1)
        selectFontButton = QPushButton("Select Font")
        selectFontButton.clicked.connect(self.chooseFont)
        notificationStyleLayout.addWidget(selectFontButton, 1, 2)
        notificationStyleLayout.addWidget(QLabel("Font Size:"), 1, 0)
        self.notificationFontSize = QLineEdit()
        self.notificationFontSize.setText(settings[1])
        self.notificationFontSize.setEnabled(False)
        notificationStyleLayout.addWidget(self.notificationFontSize, 1, 1)
        notificationFontGroupBox.setLayout(notificationStyleLayout)
        layout.addWidget(notificationFontGroupBox, 1)


        notificationStyleLayout.addWidget(QLabel("Select text color"), 2, 0)
        self.backGroundColorLineEdit = QLineEdit()
        self.backGroundColorLineEdit.setText(settings[2])
        self.backGroundColorLineEdit.setEnabled(False)
        self.textColorLineEdit = QLineEdit()
        self.textColorLineEdit.setText(settings[3])
        self.textColorLineEdit.setEnabled(False)
        notificationStyleLayout.addWidget(self.textColorLineEdit, 2, 1)
        colorPickerButton = QPushButton("Pick a color")
        colorPickerButton.clicked.connect(lambda: self.openColorPicker(self.textColorLineEdit))
        notificationStyleLayout.addWidget(colorPickerButton, 2, 2)
        notificationStyleLayout.addWidget(QLabel("Select background color"), 3, 0)
        notificationStyleLayout.addWidget(self.backGroundColorLineEdit, 3, 1)
        backGroundColorPickerButton = QPushButton("Pick a background color")
        backGroundColorPickerButton.clicked.connect(lambda: self.openColorPicker(self.backGroundColorLineEdit))
        notificationStyleLayout.addWidget(backGroundColorPickerButton, 3, 2)

        layout.addWidget(QLabel("Select a .wav file for the notification audio"))
        audioLayout = QHBoxLayout()
        self.audioFilePathLineEdit = QLineEdit()
        self.audioFileName = settings[4]
        self.audioFilePathLineEdit.setText(self.audioFileName)
        self.audioFilePathLineEdit.setEnabled(False)
        layout.addWidget(self.audioFilePathLineEdit)
        selectAudioButton = QPushButton("Select File")
        selectAudioButton.clicked.connect(self.selectAudioFile)
        audioLayout.addWidget(selectAudioButton)
        self.playAudioButton = QPushButton("Play")
        self.updatePlayButton()
        self.playAudioButton.clicked.connect(self.playAudioFile)
        audioLayout.addWidget(self.playAudioButton)

        self.exampleLabel = QLabel("This is an example.")
        self.exampleLabel.setObjectName("NotificationLabel")
        self.updateExample()
        notificationStyleLayout.addWidget(self.exampleLabel, 4, 0, 1, 3)

        layout.addLayout(audioLayout, 5)

        self.setLayout(layout)

    def updateExample(self):
        self.updateExampleColor()
        self.updateExampleFont(QFont(self.notificationFont.text(), int(self.notificationFontSize.text()), -1, False))

    def updateExampleFont(self, font):
        self.exampleLabel.setFont(font)

    def updateExampleColor(self):
        self.setStyleSheet(self.makeStyleSheet())

    def makeStyleSheet(self):
        return "QLabel#NotificationLabel { background-color : " + self.backGroundColorLineEdit.text() +  "; color : " + self.textColorLineEdit.text() + "; }"

    def openColorPicker(self, lineEdit):
        color = QColorDialog.getColor(QColor(lineEdit.text()))
        if color.isValid() and color.name(QColor.HexRgb) != lineEdit.text():
            lineEdit.setText(color.name(QColor.HexRgb))
            self.updateExample()

    def playAudioFile(self):
        QSound.play(self.audioFileName)

    def updatePlayButton(self):
        self.playAudioButton.setEnabled(os.path.exists(self.audioFileName))

    def getAudioDirectory(self):
        if os.path.exists(self.audioFileName):
            os.path.dirname(self.audioFileName)
        else:
            return os.getcwd()

    def selectAudioFile(self):
        audioFileName = QFileDialog.getOpenFileName(self, "Choose a .wav file", self.getAudioDirectory(),  "WAVE file (*.wav)")
        if audioFileName[0] != self.audioFileName:
            self.audioFileName = audioFileName[0]
            self.updatePlayButton()
            self.audioFilePathLineEdit.setText(self.audioFileName)

    def chooseFont(self):
        fontDialog = QFontDialog()
        fontDialog.setCurrentFont(QFont(self.notificationFont.text(), int(self.notificationFontSize.text()), -1, False))
        fontDialog.exec()
        self.notificationFont.setText(fontDialog.currentFont().family())
        self.notificationFontSize.setText(str(int(fontDialog.currentFont().pointSizeF())))
        self.updateExampleFont(fontDialog.currentFont())

    def saveSetting(self):
        settings = []
        settings.append(self.notificationFont.text())
        settings.append(self.notificationFontSize.text())
        settings.append(self.backGroundColorLineEdit.text())
        settings.append(self.textColorLineEdit.text())
        settings.append(self.audioFileName)
        SettingManager.saveSetting(SettingManager.NOTIFICATION_SETTING_FILE, settings)
        self.settingDialog.mainWindow.centralWidget.chatUI.chatScreen.notificationManager.updateSetting()