import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} ist online')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!ping':
        await message.channel.send('Pong!')

    if message.content == '!hi':
        await message.channel.send('Sup gng')

client.run('MTQ3OTYxNDMwNjA4ODc4MDAxNw.GBPnQg.5druvwRFFKYGnZ9r7LvW7p4N_ZeMGaGJkk-tM4')
