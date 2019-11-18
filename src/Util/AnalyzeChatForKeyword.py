class AnalyzeChatForKeyword():
    def __init__(self, channel):
        self.channel = channel
        self.count = 0
        self.Keywords = [
            "giveaway",
            "give away",
            "prize"
            ]
    #list of keywords
    def isAGiveaway():
        self.message = newMessage
    def isFound(self, user, message):
        message = message.lower()
        #checks if user is a NightBot and if any string in Keyword is found in message
        if user == "NightBot":
            for i in range(len(self.Keywords)):
                if(self.Keywords[i]) in message:
                    return True
            return False
            
        else:
            for i in range(len(self.Keywords)):
                if(self.Keywords[i]) in message:
                    self.count += 1
                    if(self.count > 4):
                        return True
            return False