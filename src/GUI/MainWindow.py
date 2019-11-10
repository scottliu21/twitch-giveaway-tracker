from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QGroupBox, QGridLayout, QFontDialog
from PyQt5.QtGui import QFont

class MainWidget(QWidget):
    def __init__(self, settingDialog):
        super(MainWidget, self).__init__(settingDialog)
        self.settingDialog = settingDialog
        self.isChanged = False
        layout = QVBoxLayout()

        file = open('setting/MainSetting', 'r')
        chatFontGroupBox = QGroupBox(self)
        chatFontGroupBox.setTitle("Chat Font")
        chatFontLayout = QGridLayout()
        chatFontLayout.addWidget(QLabel("Font Name:"), 0, 0)
        self.chatFont = QLineEdit()
        self.chatFont.setText(file.readline().strip())
        self.chatFont.setEnabled(False)
        chatFontLayout.setContentsMargins(5, 5, 5, 5)
        chatFontLayout.addWidget(self.chatFont, 0, 1)
        selectFontButton = QPushButton("Select Font")
        selectFontButton.clicked.connect(self.chooseFont)
        chatFontLayout.addWidget(selectFontButton, 1, 2)
        chatFontLayout.addWidget(QLabel("Font Size:"), 1, 0)
        self.chatFontSize = QLineEdit()
        self.chatFontSize.setText(file.readline().strip())
        self.chatFontSize.setEnabled(False)
        chatFontLayout.addWidget(self.chatFontSize, 1, 1)
        chatFontLayout.addWidget(QLabel("Line Spacing:"), 2, 0)
        self.chatLineSpacing = QLineEdit()
        self.chatLineSpacing.setText(file.readline().strip())
        self.chatLineSpacing.setEnabled(False)
        chatFontLayout.addWidget(self.chatLineSpacing, 2, 1)
        chatFontGroupBox.setLayout(chatFontLayout)
        layout.addWidget(chatFontGroupBox)

        self.setLayout(layout)
        file.close()

    def chooseFont(self):
        self.isChanged = True
        fontDialog = QFontDialog()
        fontDialog.setCurrentFont(QFont(self.chatFont.text(), int(self.chatFontSize.text()), -1, False))
        fontDialog.exec()
        self.chatFont.setText(fontDialog.currentFont().family())
        self.chatFontSize.setText(str(int(fontDialog.currentFont().pointSizeF())))

    def saveSetting(self):
        if self.isChanged:
            file = open('setting/MainSetting', 'w')
            file.truncate()
            file.write(self.chatFont.text() + '\n')
            file.write(self.chatFontSize.text() + '\n')
            file.write(self.chatLineSpacing.text())
            file.close()