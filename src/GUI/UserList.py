from PyQt5.QtWidgets import QListWidget
from GUI.Chat.User import *


class UserList(QListWidget):
    def __init__(self, parent):
        super().__init__()
        self.chatTab = parent
        self.setSortingEnabled(False)
        self.nickList = {}

    def addUser(self, nick):
        if self.nickList.get(nick, None) is None:
            userListEntry = UserListEntry(nick)
            if '#' + nick == self.chatTab.channelName:
                userListEntry.setStreamer()
            self.insertItem(self.indexOfUserInsert(userListEntry), userListEntry)
            self.nickList[nick] = userListEntry

    def updateUser(self, nick, badges, subBadge, bitsBadge, badgeSize):
        user = self.nickList[nick]
        self.removeUser(user, False)
        user.updateUserBadge(badges, subBadge, bitsBadge, badgeSize)
        self.insertItem(self.indexOfUserInsert(user), user)

    def removeUser(self, user, part):
        self.takeItem(self.indexOfUserName(user))
        if part:
            self.nickList.pop(user.nick)

    def reIndexUserForSystemModding(self, nick):
        user = self.nickList.get(nick, None)
        if user is None:
            self.addUser(nick)
            user = self.nickList[nick]
        if '@' not in user.userName:
            self.removeUser(user, False)
            user.setMod()
            self.insertItem(self.indexOfUserInsert(user), user)

    def indexOfUserInsert(self, user):
        first = 0
        last = self.count() - 1
        if last > 0:
            while first < last:
                mid = (int) ((first + last) / 2)
                if self.item(mid) < user:
                        first = mid + 1
                else:
                    if mid == 0:
                        return 0
                    else:
                        last = mid - 1
            if self.item(first) < user:
                return first + 1
            else:
                return first
        if last == -1:
            return 0
        if self.item(0) < user:
            return 1
        else:
            return 0

    def indexOfUserName(self, user):
        first = 0
        last = self.count() - 1
        while first <= last:
            mid = (int) ((first + last) / 2)
            if self.item(mid) == user:
                return mid
            else:
                if last == first:
                    break
                if self.item(mid) < user:
                    first = mid + 1
                else:
                    last = mid - 1
        return -1
