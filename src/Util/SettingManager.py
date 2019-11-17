import os


# An easy class to access settings everywhere
class SettingManager:
    SETTING_DIRECTORY = "setting/"
    MAIN_SETTING_FILE = "setting/MainSetting"
    NOTIFICATION_SETTING_FILE = "setting/NotificationSetting"
    CHAT_CSS_FILE = "setting/ChatCSS"
    DEFAULT_CHANNEL_FILE = "setting/default_channel"
    LOGIN_FILE = "setting/login"

    @staticmethod
    def setUpBasicSettingFiles():
        if not os.path.exists(SettingManager.SETTING_DIRECTORY):
            os.mkdir(SettingManager.SETTING_DIRECTORY)
        with open(SettingManager.MAIN_SETTING_FILE, 'w') as file:
            file.write("Consolas\n10\n10\n\n")
        with open(SettingManager.NOTIFICATION_SETTING_FILE, 'w') as file:
            file.write("Consolas\n10\n#ffff7f\n#000000\n\n")
        with open(SettingManager.CHAT_CSS_FILE, 'w') as file:
            file.write("QTextBrowser { background-color: black; color: white; }")

    @staticmethod
    def getUsername():
        return SettingManager.getSettingFileContent(SettingManager.LOGIN_FILE)[0]

    @staticmethod
    def saveSetting(fileName, content):
        with open(fileName, "w") as file:
            for line in content:
                file.write(line.strip() + "\n")

    @staticmethod
    def clearSettingFile(fileName):
        open(fileName, 'w').close()

    @staticmethod
    def checkBasicSettingFilesCompletion():
        try:
            with open(SettingManager.MAIN_SETTING_FILE) as file:
                if not SettingManager.checkIfFileIsCompleted(file, 3):
                    return False
            with open(SettingManager.NOTIFICATION_SETTING_FILE) as file:
                if not SettingManager.checkIfFileIsCompleted(file, 5):
                    return False
            with open(SettingManager.CHAT_CSS_FILE) as file:
                if not SettingManager.checkIfFileIsCompleted(file, 1):
                    return False
        except FileNotFoundError:
            return False
        return True

    @staticmethod
    def checkLoginFilesAreCompleted():
        try:
            with open(SettingManager.DEFAULT_CHANNEL_FILE) as file:
                if not SettingManager.checkIfFileIsCompleted(file, 1):
                    return False
            with open(SettingManager.LOGIN_FILE) as file:
                if not SettingManager.checkIfFileIsCompleted(file, 3):
                    return False
        except FileNotFoundError:
            return False
        return True

    @staticmethod
    def checkAllFilesCompletion():
        return SettingManager.checkBasicSettingFilesCompletion() and SettingManager.checkLoginFilesAreCompleted()

    # ues this if the content is not supposed to be broken up to lines
    @staticmethod
    def getHTMLSettingContent(fileName):
        with open(fileName) as file:
            return file.read()

    # use this if the content should be line by line
    # returns a list, may turn into a dict or json when I feel like to
    @staticmethod
    def getSettingFileContent(fileName):
        content = []
        with open(fileName) as file:
            for line in file:
                content.append(line.rstrip())
        return content

    @staticmethod
    def checkIfFileIsCompleted(file, miniMumLineCount):
        for _ in file:
            miniMumLineCount = miniMumLineCount - 1
        return miniMumLineCount <= 0
