#TODO - Change the simple Dict of Adventurers into a full class!
class adventure:

    def __init__(self, nameOfAdv, minPlayers, maxPlayers, ):
        self.name = nameOfAdv
        self.minPlayers = minPlayers
        self.maxPlayers = maxPlayers
        self.date = "This is a bug"
        self.time = "Also a bug"

    def setDateAndTime(self, date, time):
        self.date = date
        self.time = time

    def getStandardOutput(self):
        return f"Current list of players for {self.name} on {self.date} at {self.time}"

