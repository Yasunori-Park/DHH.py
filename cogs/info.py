# -*- coding: utf-8 -*-
#If error 429, run kill 1 in Shell
import discord
from discord.ext import commands


client = discord.Client()
client = commands.Bot(command_prefix='!')
client.remove_command("help")
intents = discord.Intents.default()
intents.members = True

class info(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  #!Info 1-3
  @commands.command()
  async def info(self, ctx):
    await ctx.channel.send("Daz is a little slow today. Right now he can respond if you say: \n**Hi Daz** \n**Inspire me Daz**\n'**!info2**' for commands Daz can do\n'**!info3**' for pasta\n'**!infoEcon**' for info about the points system\n '**!infoDnD**' for info about the DnD system (WIP)")
    
  @commands.command()
  async def info2(self, ctx):
    await ctx.channel.send("Daz can do the following commands: \n'**!weather (any city)**' to find the forecast of a city\n'**!typewriter (number)**' to have a go at the Infinite monkey theorem\n**!top10val** to scan the top 10 players on the Asia-Pacific valorant leaderboard\n**!qr (url)** to generate a QR code for a link (idk)\n**!google (any search terms)** to generate a link to a google search")
    
  @commands.command()
  async def info3(self, ctx):
    await ctx.channel.send("Daz can send pasta with the following commands:\n**!rounds (somebody's name)**\n**!throw (somebody's name)** (*2 options*)\n**!uninstall (game title**)\n**!Lunarman**\n**!Ake**\n**!Eunbi**\n**!Issa**\n**!Daiwa**\n**!Nori**\n**bear**\n**prime**\n**Rammus/@OK/armadillo**\n**formula 1**\n**grammar**\n**Daz what should I do today?** (*3 options*)")
    
  @commands.command()
  async def infoEcon(self, ctx):
    await ctx.channel.send("Daz has opened up a bank trading in valueless points.\n'**!balance**' to open a DazBank account or to check the number of points you have\nTo donate or trade points to somebody with a DazBank: '**!donate (@user) n(any amount less than your total balance)**'\nTo get a loan with no strings attached, with no repayment fees (:>) '**!loan n(any amount <100 points)**'\n'**!points_loaned**' to see how many points registered users have earned from loans\n'**!infobet**' for an explanation of the '**!bet**' function\n'**!bets_won**' to see how many points all registered users have won from **!bet**\n'**!leader**' to see who has the most points out of all registered users.")
    
  @commands.command()
  async def infobet(self, ctx):
    await ctx.channel.send("The '**!bet**' function has the following input:\n'**!bet' @user (user you wish to wager against) x (x = number of points to wager) (Bet you made)**\nBets made will need to be either Yes or No, with the correct answer being Yes\nBets are counted as successful if Yes votes > (No + 1) votes\nSuccessful bets will result in x points being taken from the @user's points balance\nFailed bets will result in x points being donated to the @user's points balance from your balance.")

  @commands.command()
  async def infoDnD(self, ctx):
    await ctx.channel.send("Daz bot is being set up to create a DnD game that can be run exclusively from discord!\n'**!roll x y**' to roll a die, where x = number of sides of the die, y = how many times you want to roll.\n'**!NewBlood**' to randomly generate a character. Each NewBlood entry is tied to a user's discord account so be careful if you roll a good one!\n'**!passport (username)**' to see the character sheet for a character assigned to unit. Try '**!passport Ake**' as an example. You can also pass '**!passport me**' to see your own character sheet.\n'**!rewrite (username) (stat) (new argument)**' to change certain features of your character! Type !info_rewrite to see more.\n'**!levelup**' to change the stats of your character. Type !info_levelup to see more.\n'**!damage (username) (amount of damage)**' to indicate a character has taken damage. If it goes below 0 the character will automatically be assigned as Dead.\n'**!heal (username) (amount of healing)**' to indicate a character has been healed. Healing cannot exceed max hp.\n'**!spell (spell name)**' to search the DnD 5e api for the details of a spell (if it is recorded).\n'**!pandora**' for what is the pandora boss.\n'**!summon_pandora**' to summon a randomly generated boss from pandora's box :D\n'**!check_pandora**' to see the details of the boss summoned.")

  @commands.command()
  async def info_rewrite(self, ctx):
    await ctx.channel.send("Example input:\n\n*!rewrite LunarMan weapon RA THE SUN GOD*\n\nWith !rewrite you *cannot* change the character's **species**, **age**, **height**, **weight** or **size**. If you really want to, let the DM know.\nStatus is (for now) set to only accept the arguments: Alive, Dead or Afflicted.\nClasses can be changed only to one of the following: **Barbarian**, **Bard**, **Cleric**, **Druid**, **Fighter**, **Monk**, **Paladin**, **Ranger**, **Rogue**, **Sorcerer**, **Warlock**, or **Wizard**\nIf you'd like to change your name, pass the stat as: first_name or last_name.\n\nStats such as max_hp, level, exp, str etc. are changed via !levelup (!info_levelup)")

  @commands.command()
  async def info_levelup(self, ctx):
    await ctx.channel.send("Example input:\n\n*!levelup LunarMan exp 999999999*\n\nWith !levelup you can change stats that have a numerical value e.g. max_hp, consitution, dexterity etc.\n\nTo change values such as first_name, last_name, weapon, armour; use !rewrite (!info_rewrite)") 

  @commands.command()
  async def pandora(self, ctx):
    await ctx.channel.send('Pandora was a beautiful self-made trillionaire from the distant future, who claimed to have made her fortune selling "NFT"s of "Pokeman cards". Using her fortune, she made a one-way time travelling device that sent her to the current time period, and tried to make herself ruler of all living beings. Bitter nobody understood the value of her .jpgs, she recruited people into her order of "Tier 3 Twitch White-Knights" and used the power of drugs and the arcane to turn them all into powerful beasts; Every single one unique, wielding weapons uncommon to this time period.\nA hundred years ago the greatest hero the world has seen; Lukas Unarman, defeated Pandora and sealed all her beasts away. These beasts however, lie inside their seals, waiting for the day they are released and can destroy the world. Adventurers close to Daz have been tasked with taking on a beast of Pandora if they are so brave enough...')


def setup(client):
  client.add_cog(info(client))
