import discord
from discord.ext import commands

class Adventure:

    def __init__(self, nameOfAdv, minPlayers, maxPlayers, ):
        self.name = nameOfAdv
        self.minPlayers = minPlayers
        self.maxPlayers = maxPlayers
        self.date = "This is a bug"
        self.time = "Also a bug"
        self.scheduled = False
        self.lastOutput = ""

    def setDateAndTime(self, date, time):
        self.date = date
        self.time = time
        self.scheduled = True

    def getStandardOutput(self):
        if self.scheduled == True:
            return f"Current list of players for {self.name} on {self.date} at {self.time}"
        return f"{self.name} has not been scheduled"

    def setLastOutput(self, lastOutput):
        self.lastOutput = lastOutput

    def getCurrentOutput(self, users):
        output = self.getStandardOutput()
        for user in users:
            output += '\n' + user.mention
        output += '\n'
        self.lastOutput = output
        return output