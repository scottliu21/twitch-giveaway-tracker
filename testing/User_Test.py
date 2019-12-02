import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from GUI.Chat.User import UserListEntry


class User_Test(unittest.TestCase):

    def test_inequality(self):
        userA = UserListEntry("a")
        userB = UserListEntry("b")
        self.assertNotEqual(userA, userB)

    def test_less(self):
        userA = UserListEntry("@a")
        userB = UserListEntry("b")
        self.assertTrue(userA < userB)

    def test_greater(self):
        userA = UserListEntry("~a")
        userB = UserListEntry("%a")
        self.assertTrue(userA > userB)

    def test_equal(self):
        userA = UserListEntry("%a")
        userB = UserListEntry("%a")
        self.assertTrue(userA == userB)

if __name__ == '__main__':
    unittest.main()