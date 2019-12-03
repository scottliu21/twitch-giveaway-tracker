class AnalyzeChatForKeyword():
    def __init__(self):
        self.count = 0
        #list of keywords
        self.Keywords = [
            "giveaway",
            "give away",
            "prize"
            ]
        self.Dict = {}
        self.isFound = False;


    def isFound(self):
        return self.isFound
    #isFound logs all of message into a dictionary as well as checks for instances of keywords
    def checkIfFound(self, user, message):
        message = message.lower()
        #checks if user is a NightBot and if any string in Keyword is found in message, 
        # or if dictionary is exceeded
        for i in message:
            if not self.Dict.has_key(message[i]):
                self.Dict[i] = 1
            else:
                val = self.Dict.pop(i)
                self.Dict[i] = val + 1
                if val + 1 > 50:
                    self.isFound = True
                    return True


        if user == "NightBot":
            for i in range(len(self.Keywords)):
                if(self.Keywords[i]) in message:
                    self.isFound = True
                    return True
            return False
            
        else:
            for i in range(len(self.Keywords)):
                if(self.Keywords[i]) in message:
                    self.count += 1
                    if(self.count > 4):
                        self.isFound = True
                        return True
            return False
