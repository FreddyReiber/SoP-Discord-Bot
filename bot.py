import os
import discord
import random
from GuildFund import GuildFund
from adventure import Adventure
from dotenv import load_dotenv

from discord.ext import commands

#env info
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
EMOJI = os.getenv('DISCORD_CUSTOM_EMOJI')

#creaties the Bot
bot = commands.Bot(command_prefix='!')


#Variables for running of Bot
listOfGuildFunds = []
listOfAdventures = []
headRole = "Dungeon Master"
channelList = []


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} has connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

#Test commands
@bot.command(name = 'lol', help = 'This is for testing')
@commands.has_role(headRole)
async def on_message(ctx):
    response = "HAHAHAHAHAHAHAH, jk not that funny"
    await ctx.send(response)

#Dice Rolling Feature - All can use
#TODO Add feature to roll multiple dice
@bot.command(name = "roll", help = "Rolls a standard DnD Dice!")
async def on_message(ctx, dice):
    diceSize = 0
    if dice == 'd2':
        diceSize = 2
    elif dice == 'd4':
        diceSize = 4
    elif dice == 'd6':
        diceSize = 6
    elif dice == 'd8':
        diceSize = 8
    elif dice == 'd10':
        diceSize = 10
    elif dice == 'd12':
        diceSize = 12
    elif dice == 'd20':
        diceSize = 20
    elif dice == 'd100':
        diceSize = 100
    else:
        await ctx.send("Dice size not found")
        return
    value = random.randint(1, diceSize)
    await ctx.send(f'You rolled a {value}')


#All commands relating to the schedule feature
@bot.command(name = 'setChannel')
@commands.has_role(headRole)
async def on_message(ctx):
    channelList.append(ctx.channel)
    print(type(ctx.channel))
    await ctx.send("Set this as the channel!")

#Schedueling Commands!
#TODO make a system for keeping jobs active upon restart.
@bot.command(name = "advAdd", help = "Adds a new adventure to the list of available adventures with player count.")
@commands.has_role(headRole)
async def on_message(ctx, adventureName, minPlayers: int, maxPlayers: int):
    newAdv = Adventure(adventureName, minPlayers, maxPlayers)
    listOfAdventures.append(newAdv)
    await ctx.send(f'Added {adventureName}')

@bot.command(name = "advList", help = "Lists all currently available adventures!")
async def on_message(ctx):
    if len(listOfAdventures) == 0:
        await ctx.send("It seems there are now playable adventures right now. If you believe this is a bug, please contact Freddy!")
        return
    output = "Current List of all Adventures!\n"
    for adv in listOfAdventures:
        output += f' -{adv.name}\n'
    await ctx.send(output)

@bot.command(name = "advPlay", help = "Creates an instance of the adventure and posts it to the current job listings channel.")
async def on_message(ctx, advName, date, time):
    listIndex = -1
    for i in range(0, len(listOfAdventures)):
        if advName == listOfAdventures[i].name:
            listIndex = i

    if listIndex == -1:
        await ctx.send("That adventure is not currently in the database!")
        return
    thisAdv = listOfAdventures[listIndex]
    thisAdv.setDateAndTime(date, time)
    output = thisAdv.getStandardOutput()
    thisAdv.setLastOutput(output)
    await channelList[0].send(content = output)

@bot.event
async def on_reaction_add(ctx, user):
    if str(ctx.emoji) != EMOJI:
        return
    inList = -1
    for i in range(0, len(listOfAdventures)):
        if ctx.message.content in listOfAdventures[i].lastOutput:
            inList = i
            break
    if inList == -1:
        return

    thisAdv = listOfAdventures[inList]
    listOfUsers = await ctx.users().flatten()
    output = thisAdv.getCurrentOutput(listOfUsers)
    await ctx.message.edit(content = output )

@bot.event
async def on_reaction_remove(ctx,user):
    print("CONSOLE:: Trigger of on_reaction_remove")
    if str(ctx.emoji) != EMOJI:
        return
    inList = -1
    for i in range(0, len(listOfAdventures)):
        if ctx.message.content in listOfAdventures[i].lastOutput:
            inList = i
            break
    if inList == -1:
        return

    thisAdv = listOfAdventures[inList]
    listofUsers = await ctx.users().flatten()
    output = thisAdv.getCurrentOutput(listofUsers)
    await ctx.message.edit(content = output)
#end adv commands

#Begin Guild Fund Feature
#TODO allow for multipul guild funds to be created.
@bot.command(name = "fundCreate", help = "Initilizes a guild fund")
async def on_message(ctx, guildName, currentfunds):
    newGuildFund = GuildFund(guildName, currentfunds)
    listOfGuildFunds.append(newGuildFund)
    await ctx.send(f"Created a Guild fund for {guildName}")

@bot.command(name = "fundAdd", help = "Adds to guild fund")
async def on_message(ctx, newFunds : int):
    currentFund = listOfGuildFunds[0]
    currentFund.addGuildFunds(newFunds)
    await ctx.send(f"Add {newFunds} to the guild fund")

@bot.command(name = "fundRemove", help = "Removes from the guild fund")
async def on_message(ctx, spentFunds:int):
    currentFund = listOfGuildFunds[0]
    currentFund.removeGuildFunds(spentFunds)
    await ctx.send(f"Removed {spentFunds} from the guild fund")

@bot.command(name = "fundCheck", help = "Checks the guild fund")
async def on_message(ctx):
    currentFund = listOfGuildFunds[0]
    check = currentFund.getCurrentFunds()
    await ctx.send(f"The Guilds current funds are at {check} GP")








#Error handeling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("Sorry lad, it looks like you don't have the ability to do that.")



bot.run(TOKEN)
