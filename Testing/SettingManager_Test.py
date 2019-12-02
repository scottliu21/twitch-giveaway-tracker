import sys
import os
import shutil
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from Util.SettingManager import SettingManager


def test_setUpBasicSettingFiles(tmpdir):
    SettingManager.SETTING_DIRECTORY = tmpdir
    SettingManager.MAIN_SETTING_FILE = tmpdir + "\\MainSetting"
    SettingManager.NOTIFICATION_SETTING_FILE = tmpdir + "\\NotificationSetting"
    SettingManager.CHAT_CSS_FILE = tmpdir + "\\ChatCSS"
    SettingManager.setUpBasicSettingFiles()
    assert SettingManager.CHAT_CSS_FILE.read() == "QTextBrowser { background-color: black; color: white; }", "set up basic setting files failed: chat css file"
    assert SettingManager.NOTIFICATION_SETTING_FILE.read() == "Consolas\n10\n#ffff7f\n#000000\n\n", "set up basic setting files failed: notification setting file"
    assert SettingManager.MAIN_SETTING_FILE.read() == "Consolas\n10\n10\n\n", "set up basic setting files failed: main setting file"

def test_getUsername(tmpdir):
    p = tmpdir.join("login")
    p.write("content")
    SettingManager.LOGIN_FILE = tmpdir + "\\login"
    assert SettingManager.getUsername() == "content", "get username test failed"


def test_checkIfFileIsCompleted(tmpdir):
    p = tmpdir.join("login")
    p.write("content\ncontent\n")
    file = open(p, "r")
    assert SettingManager.checkIfFileIsCompleted(file, 0) == True
    file.close()