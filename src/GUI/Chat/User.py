from PyQt5.QtWidgets import QListWidgetItem
import random
import re

class UserListEntry(QListWidgetItem):
    DEFAULT_COLOR = ['#FF0000', '#00FF00', '#0000FF', '#B22222', '#FF7F50', '#9ACD32', '#FF4500', '#2E8B57', '#DAA520', '#D2691E', '#5F9EA0', '#1E90FF', '#FF69B4', '#8A2BE2', '#00FF7F']

    def __init__(self, nick):
        super().__init__()
        self.userName = nick
        #CHANGE THIS LATER
        self.nick = nick
        self.setText(nick)
        self.point = 0
        self.hasSpoken = False
        self.modSet = False
        self.badges = ''

    def updateUserBadge(self, badges, subBadge, bitsBadge, height):
        self.userName = self.nick
        imagePrefix = '<img ' + height + ' src="'
        self.badgesImage = ""
        if 'turbo' in badges:
            self.userName = '+' + self.userName
            self.badgesImage = imagePrefix + 'Icon/turbo.png">' + self.badgesImage
        if 'premium' in badges:
            self.userName = '+' + self.userName
            self.badgesImage = imagePrefix + 'Icon/premium.png">' + self.badgesImage
        if 'partner' in badges:
            self.badgesImage = imagePrefix + 'Icon/partner.png">' + self.badgesImage
        if 'bits/' in badges:
            self.userName = '$' + self.userName
            amount = re.search(re.compile('.*bits/(\d+)'), badges)
            if amount in bitsBadge:
                self.badgesImage = imagePrefix + bitsBadge[amount.group(1)] + '">' + self.badgesImage
            else:
                self.badgesImage = imagePrefix + 'Icon/bits ' + amount.group(1) + '.png">' + self.badgesImage
        if 'subscriber' in badges:
            self.userName = '%' + self.userName
            if len(subBadge) > 0:
                self.badgesImage = imagePrefix + subBadge[re.search(re.compile('subscriber/(\d+)'), badges).group(1)] + '">' + self.badgesImage
            else:
                self.badgesImage = imagePrefix + 'Icon/subscriber.png">' + self.badgesImage
        if 'moderator' in badges:
            self.userName = '@' + self.userName
            self.badgesImage = imagePrefix + 'Icon/moderator.png">' + self.badgesImage
        if 'global_mod' in badges:
            self.userName = '*' + self.userName
            self.badgesImage = imagePrefix + 'Icon/globalmod.png">' + self.badgesImage
        if 'admin' in badges:
            self.userName = '!' + self.userName
            self.badgesImage = imagePrefix + 'Icon/admin.png">' + self.badgesImage
        if 'staff' in badges:
            self.userName = '&' + self.userName
            self.badgesImage = imagePrefix + 'Icon/staff.png">' + self.badgesImage
        if 'broadcaster' in badges:
            self.userName = '~' + self.userName
            self.badgesImage = imagePrefix + 'Icon/broadcaster.png">' + self.badgesImage
        self.setText(self.userName)
        self.calculatePoint()
        self.badges = badges

    def updateUserColor(self, color):
        if color:
            #change it to check back ground color
            if color == "#000000":
                self.randomColor = False
                self.color = "#808080"
            else:
                self.randomColor = False
                self.color = color
        else:
            self.randomColor = True
            self.color = random.choice(UserListEntry.DEFAULT_COLOR)

    def setStreamer(self):
        self.userName = '~' + self.userName
        self.calculatePoint()
        self.setText(self.userName)

    def setMod(self):
        if self.modSet == False and self.hasSpoken == False:
            if self.userName[0] != '~':
                self.userName = '@' + self.userName
            self.setText(self.userName)
            self.calculatePoint()
            self.modSet = True


    def calculatePoint(self):
        self.point = 0
        if '~' in self.userName:
            self.point += 16
        if '&' in self.userName:
            self.point += 8
        if '!' in self.userName:
            self.point += 8
        if '*' in self.userName:
            self.point += 4
        if '@' in self.userName:
            self.point += 2
        if '%' in self.userName:
            self.point += 1

    def __lt__(self, other):
        if self.point == other.point:
            return self.nick < other.nick
        return self.point > other.point

    def __gt__(self, other):
        if self.point == other.point:
            return self.nick > other.nick
        return self.point < other.point

    def __eq__(self, other):
        return self.nick == other.nick

    def setUserChat(self, userChat):
        self.userChat = userChat