class GuildFund:

    #Init Method
    def __init__(self, guildName, startingFunds : int):
        self.guildName = guildName
        self.funds = startingFunds

    #Getter and Setters

    def getCurrentFunds(self):
        return self.funds

    def getGuildName(self):
        return self.guildName

    #Adds funds and returns current funds.
    def addGuildFunds(self, newFunds : int):
        self.funds += newFunds
        return self.funds

    def removeGuildFunds(self, spentFunds : int):
        self.funds -= spentFunds
        return self.funds

