import os
import discord
import random
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} has connect to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

@bot.command(name = 'lol', help = 'This is for testing')
async def on_message(ctx):
    response = "HAHAHAHAHAHAHAH, jk not that funny"
    await ctx.send(response)

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
    elif dice == 'd20':
        diceSize = 20
    elif dice == 'd100':
        diceSize = 100
    else:
        await ctx.send("Dice size not found")
        return
    value = random.randint(1, diceSize)
    await ctx.send(f'You rolled a {value}')

bot.run(TOKEN)
