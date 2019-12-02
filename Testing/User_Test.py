import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from GUI.Chat.User import UserListEntry


def test_inequality():
    userA = UserListEntry("a")
    userB = UserListEntry("b")
    assert userA != userB, "inequality test failed"


def test_less():
    userA = UserListEntry("@a")
    userB = UserListEntry("b")
    assert userA < userB, "less than test failed"


def test_greater():
    userA = UserListEntry("~a")
    userB = UserListEntry("%a")
    assert userA > userB, "greater than test failed"


def test_equal():
    userA = UserListEntry("%a")
    userB = UserListEntry("%a")
    assert userA == userB, "equality test failed"
