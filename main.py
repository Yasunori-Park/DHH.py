# -*- coding: utf-8 -*-
#If error 429, run kill 1 in Shell
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from uptime_ping import keep_Daz_running
import Daz_activity as D
import json
import os
import nacl
import pytz
import random
import requests


client = discord.Client()
client = commands.Bot(command_prefix='!')
client.remove_command("help")
intents = discord.Intents.default()
intents.members = True


#variables
cogs = []
Ram_ok = ["Rammus", "@OK", "armadillo"]
f1 = ["Formula 1", "F1" ,"Gentlemen", "gentlemen"]


for filename in os.listdir("./cogs"):
  if filename.endswith('.py'):
    cogs.append("cogs." + filename[:-3])

if __name__ == '__main__':
  for cog in cogs:
    client.load_extension(cog)
    print(cog)


among_us_emojis = []
def among_us():
    for guild in client.guilds:
        for emoji in guild.emojis:
            name = emoji.name.lower()
            if "amongus" in name or "among_us" in name or "sus" in name:
                among_us_emojis.append(emoji)

@client.event
async def on_ready():
    print('Daz bot is ready to download a car')
    among_us()

@client.event
async def setup():
    await client.wait_until_ready()
    if True:
      print("DazBank is online")
    else:
      print("DazBank is offline")
client.loop.create_task(setup())

def get_inspire_author_Daz():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "\n -Daz"
  return(quote)

  

##Daz responses
@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return

    if message.content =='Hi Daz':
        await message.channel.send('Hello little one.')

    for i in Ram_ok:
      if i in message.content:
        await message.channel.send(D.Rammus)
  
    if 'prime' in message.content:
        await message.channel.send(D.prime)

    if 'bear' in message.content:
      await message.channel.send(D.Volibear)

    for i in f1:
      if i in message.content:
        await message.channel.send(D.F1)
      
    if message.content == "Daz what should I do today?":
      await message.channel.send(random.choice(D.Daz_activity_options))

    if "grammar" in message.content:
      await message.channel.send(random.choice(D.Grammarly))

    if "gramar" in message.content:
      await message.channel.send("Uh oh, looks like somebody needs grammarly!")
      await message.channel.send(random.choice(D.Grammarly))
  
    if message.content == "Inspire me Daz":
      quote = get_inspire_author_Daz()
      await message.channel.send(quote)

    if "Daran" in message.content:
            await message.add_reaction("<:FeelsCryMan:931366167417872394>")

  
    among_us_txt = message.content.lower()
    if "among us" in among_us_txt or "sus" in among_us_txt:
        num = random.randrange(1, len(among_us_emojis) + 1)
        if num > 0:
            await message.add_reaction(among_us_emojis[num - 1])
    

keep_Daz_running()
client.run(os.getenv('Daz_Token'))