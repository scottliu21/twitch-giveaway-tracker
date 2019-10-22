from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

class JoinChannelDialog(QDialog):
    def __init__(self, chatUI):
        super(JoinChannelDialog, self).__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.chatUI = chatUI
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('Join Channel')
        position = self.chatUI.centralWidget.mainWindow.getPopUpPosition(300, 200)
        self.setGeometry(position.x(),position.y(), 300, 200)

        layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        label = QLabel()
        label.setText('Channel: ')
        entryBox = QLineEdit()
        joinButton = QPushButton()
        joinButton.setText('Join Channel')
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

    def joinChannelMessage(self):
        message = self.entryBox.text().lower().strip()
        if message is not '':
            self.chatUI.chatScreen.joinChannel(message)
        self.close()