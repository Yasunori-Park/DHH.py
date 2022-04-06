# -*- coding: utf-8 -*-
#If error 429, run kill 1 in Shell
import discord
from datetime import datetime
from discord.ext import commands
import Daz_activity as D
import json
import bs4
import os
import pytz
import random
import requests
import pyqrcode

client = discord.Client()
client = commands.Bot(command_prefix='!')
client.remove_command("help")
intents = discord.Intents.default()
intents.members = True
weather_url = "http://api.openweathermap.org/data/2.5/weather?"

##Info2 Commands
class info2(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.command()
  async def weather(self, ctx, city):
    city = str(city)
    timezone = pytz.timezone('Australia/Sydney') 
    now = datetime.now(timezone)
    now_format = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    complete_url = weather_url + "appid=" + os.getenv('weather_key') + "&q=" + city + "&units=metric"
    response = requests.get(complete_url)
    json_data = json.loads(response.text)
    Location = json_data['name'] + ", " +  json_data['sys']['country']
    Celsius = str(round(json_data['main']['temp'], 2)) + "°C"
    Feel = str(round(json_data['main']['feels_like'], 2)) + "°C"
    Humidity = str(round(json_data['main']['humidity'])) + "%"
    Forecast = json_data['weather'][0]['main']
    if "Rain" in Forecast:
      Forecast2 = Forecast + ".\nMake sure to bring an umbrella!"
    else:
      Forecast2 = Forecast + "."
    await ctx.send("At " + now_format + " (Sydney time):\nThe temperature in " + Location + " is roughly " + Celsius + ". \nHowever, today the forecast may feel like " + Feel + ". \nHumidity is at " + Humidity + ". \nThe description for today is: " + Forecast2)

  @commands.command()
  async def typewriter(self, ctx, number):
    number = int(number)
    monke = []
    for i in range(0,number):
      monke.append(random.choice(D.Shakespeare_monkey))
    await ctx.send("Shakespeare's monkey wrote: " + ''.join(monke))
    return

  @commands.command()
  async def top10val(self, ctx):
    complete_url_val = "https://ap.api.riotgames.com/val/ranked/v1/leaderboards/by-act/d929bc38-4ab6-7da4-94f0-ee84f8ac141e?size=10&startIndex=0&api_key=" + os.getenv('riot_key')
    response = requests.get(complete_url_val)
    raw_riot = json.loads(response.text)
    timezone = pytz.timezone('Australia/Sydney') 
    now = datetime.now(timezone)
    now_format = str(now.strftime("%d/%m/%Y %H:%M:%S"))
    Name = []
    for player in raw_riot['players']:
      if 'leaderboardRank' in player:
          Name.append("Rank " + str(player['leaderboardRank']) + ": ")
      else:
          Name.append("No rank listed")
      if 'gameName' in player:
          Name.append(player['gameName'] + " with")
      else:
          Name.append("Secret Agent" + " with")
      if 'numberOfWins' in player:
          Name.append(str(player['numberOfWins']) + " wins")
      else:
          Name.append("no wins recorded")
    List = iter(Name)
    Name2 = list(zip(List, List, List)) 
    await ctx.send("The top 10 players on the AP Valorant leaderboards @ " + now_format + " are:\n" + str(Name2).replace("[", "")
                     .replace(")", "\n")
                     .replace("(", "")
                     .replace(",", "")
                     .replace("'", "")
                     .replace("]", ""))

  @commands.command()
  async def qr (self, ctx, url):
    url = str(url)
    user = ctx.author
    url2 = pyqrcode.create(url)
    url2.png("QR.png", scale=10)
    em = discord.Embed(colour = discord.Colour(0xffffff))
    em.set_author(name = f"{ctx.author.display_name} made this QR code", icon_url=user.avatar_url)
    file = discord.File(".//image//QR.png", filename="QR.png")
    em.set_image(url="attachment://QR.png")
    await ctx.send(file=file, embed=em)

  @commands.command()
  async def google (self, ctx, *, arg="Testing"):
    google_url = "https://www.google.com.au/search?q="
    message = arg 
    query = message.replace(" ", "+")
    query2 = (google_url + query)
    await ctx.send(query2 + "\nThe first result from the above google search is:\n")
    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"}
    search = requests.get(query2, headers=headers)
    empty = []
    empty2 = []
    soup = bs4.BeautifulSoup(search.text,
                         "lxml")
    for result in soup.select('.tF2Cxc'):
      title = result.select_one('.DKV0Md').text
      link = result.select_one('.yuRUbf a')['href']
      empty.append(title)
      empty2.append(link)
    await ctx.send(empty[0] + "\n" + empty2[0])
    

def setup(client):
  client.add_cog(info2(client))