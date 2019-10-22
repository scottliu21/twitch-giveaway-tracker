from PyQt5.QtWidgets import QLineEdit
import re
import random

class EntryBox(QLineEdit):
    whisperSentFormat = '/w ([^ ]+) (.*)'
    def __init__(self, parent, chatScreen):
        super(EntryBox, self).__init__(parent)
        self.chatScreen = chatScreen
        self.returnPressed.connect(self.send)
        self.setFont(self.chatScreen.font)
        self.rainbow = False

    def send(self):
        channelName = self.chatScreen.widget(self.chatScreen.currentIndex()).channelName
        self.setText(self.text().strip())
        if self.text().startswith('/w'):
            if self.text().count(' ') > 1:
                result = re.search(EntryBox.whisperSentFormat, self.text())
                whisperReciver = result.group(1).lower()
                whisperChat = self.chatScreen.tabs.get('$' + whisperReciver, None)
                if whisperChat is None:
                    whisperChat = self.chatScreen.newWhisperChat(whisperReciver)
                whisperChat.newSentMessage(result.group(2))
                self.chatScreen.clientIRC.sendMessage('PRIVMSG #jtv :/w ' + whisperReciver + ' ' + result.group(2) + '\r\n')
        elif self.text().startswith('/rainbow'):
            if not self.rainbow:
                self.chatScreen.clientIRC.sendMessage('PRIVMSG #jtv :/color #000000\r\n')
            self.rainbow = not self.rainbow
        elif '#' in channelName:
            self.chatScreen.clientIRC.sendMessage('PRIVMSG ' + channelName + " :" + self.text() + '\r\n')
        else:
            self.chatScreen.clientIRC.sendMessage('PRIVMSG #jtv :/w ' + channelName[1:] + ' ' + self.text() + '\r\n')
            whisperChat = self.chatScreen.tabs[channelName]
            whisperChat.newSentMessage(self.text())
        self.setText('')
        if self.rainbow:
            color = self.randomColor()
            print(color)
            self.chatScreen.clientIRC.sendMessage('PRIVMSG #jtv :/color ' + color + '\r\n')

    def randomColor(self):
        letters = '0123456789ABCDEF'
        color = '#'
        for x in range(0, 6):
            color += random.choice(letters)
        return color
