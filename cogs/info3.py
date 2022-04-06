# -*- coding: utf-8 -*-
#If error 429, run kill 1 in Shell
import discord
from discord.ext import commands
import Daz_activity as D
import random

client = discord.Client()
client = commands.Bot(command_prefix='!')
client.remove_command("help")
intents = discord.Intents.default()
intents.members = True

##info3 prompts
class info3(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.command()
  async def throw(self, ctx, user : discord.Member):
    throw1 = (D.throw_pasta_1_1 + user.mention + D.throw_pasta_1_2)
    throw2 = ("Hey" + user.mention + D.throw_pasta_2_1 )
    throw_list = [throw1, throw2]
    await ctx.send(random.choice(throw_list))

  @commands.command()
  async def rounds(self, ctx, user: discord.Member):
    await ctx.send("When both teams are even in rounds, " + user.mention + " feels that they are at a great advantage and thus they do not hesitate to run in 1 v 5. When " + user.display_name + "'s team is 3 rounds behind, " + user.display_name + " thinks that they are at a small advantage, and so they force buy an Operator to secure their 'lead'. When " + user.display_name + "'s team is 7 rounds behind, " + user.display_name +" thinks they are at a disadvantage and so they look for a 1 v 5 engage to regain control of the game. When " + user.display_name + "'s team is 10 rounds behind, " + user.display_name + " thinks that the team has reached a desperate situation and they are only waiting passively for their death if they do not go in 1 v 5.")

  @commands.command()
  async def uninstall(self, ctx, *game):
    separator = " "
    game = separator.join(game)
    game = str(game)
    game = game.upper()
    await ctx.send(D.Uninstalling_1 + game + D.Uninstalling_2)

  @commands.command()
  async def Lunarman(self, ctx):
    await ctx.send(D.LunarMan)
  
  @commands.command()
  async def Ake(self, ctx):
    await ctx.send(D.Ake)
  
  @commands.command()
  async def Eunbi(self, ctx):
    await ctx.send(D.Eunbi)
  
  @commands.command()
  async def Issa(self, ctx):
    await ctx.send(D.Issa)
  
  @commands.command()
  async def Daiwa(self, ctx):
    await ctx.send(D.Daiwa)
  
  @commands.command()
  async def Nori(self, ctx):
    await ctx.send(D.Nori)

def setup(client):
  client.add_cog(info3(client))