import discord
from discord.ext import commands
import nacl

#Functionality of class Sound is limited as Replit doesn't support audio related libraries

class Sound(commands.Cog):
    def __init__(self, client):
      self.client = client
      self._last_member = None
  
    @commands.command(pass_context=True)
    async def join(self, ctx):
      Daz_join = ctx.author.voice
      if Daz_join:
        await Daz_join.channel.connect()
      else:
        await ctx.send("You need to join a voice channel first")
  
    @commands.command()
    async def leave(self, ctx):
      Daz_leave = ctx.voice_client
      if Daz_leave:
        await Daz_leave.disconnect()
      else:
        await ctx.send("Daz is not connected to a channel")



def setup(client):
  client.add_cog(Sound(client))