# -*- coding: utf-8 -*-
#If error 429, run kill 1 in Shell
import discord
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import Bot
import Daz_activity as D
import json
import os
import nacl
import pytz
import random
import requests
import asyncio

client = discord.Client()
client = commands.Bot(command_prefix='!')
client.remove_command("help")
intents = discord.Intents.default()
intents.members = True
  
#Class
class Economy(commands.Cog):
  def __init__(self, client):
    self.client = client
    

  async def get_bank_data(self):
    with open("Bank.json", "r") as f:
      users = json.load(f)
    return users

  async def open_account(self, user):
    users = await self.get_bank_data()
    if str(user.id) in users:
      return False
    else:
      users[str(user.id)] = {}
      users[str(user.id)]["ID"] = user.name
      users[str(user.id)]["points"] = 100
      users[str(user.id)]["colour"] = random.choice(D.colours)
      users[str(user.id)]["loans"] = 0
      users[str(user.id)]["wins"] = 0
    with open("Bank.json", "w") as f:
      json.dump(users,f)
    return True
    
  async def update_bank(self, user, change = 0, mode = "points"):
    users = await self.get_bank_data()
    users[str(user.id)][mode] += change
    with open("Bank.json", "w") as f:
      json.dump(users, f)
      bal = users[str(user.id)]["points"]
    return bal

  async def update_win(self, user, change = 0, mode = "wins"):
    users = await self.get_bank_data()
    users[str(user.id)][mode] += change
    with open("Bank.json", "w") as f:
      json.dump(users, f)
      w_bal = users[str(user.id)]["wins"]
    return w_bal
  
  @commands.command()
  async def balance(self, ctx):
    timezone = pytz.timezone('Australia/Sydney') 
    now = datetime.now(timezone)
    user = ctx.author
    await self.open_account(ctx.author)
    users = await self.get_bank_data()
    points_amount = users[str(user.id)]["points"]
    col = users[str(user.id)]["colour"]
    em = discord.Embed(colour =  discord.Colour(int(f"0x{col}", 16)))
    em.set_author(name = f"{ctx.author.display_name}'s balance", icon_url=user.avatar_url)
    em.add_field(name = "Points", value = points_amount)
    file = discord.File(".//image//teller2.jpg", filename="teller2.jpg")
    em.set_image(url="attachment://teller2.jpg")
    em.timestamp = now
    await ctx.send(file=file, embed = em)
  
  @commands.command()
  async def donate(self, ctx, member:discord.Member, amount = None):
      await self.open_account(ctx.author)
      await self.open_account(member)
      amount = int(amount)
      timezone = pytz.timezone('Australia/Sydney') 
      now = datetime.now(timezone)
      if amount == None:
          await ctx.send("Please enter the amount")
          return
      bal = await self.update_bank(ctx.author)
      if amount>bal:
          await ctx.send("You don't have that much points")
          return
      if amount<=0:
          await ctx.send("DazBank can only donate positive amounts")
          return
      await self.update_bank(ctx.author, -1*amount, "points")
      await self.update_bank(member, 1*amount, "points")
      em = discord.Embed(description = f"On behalf of {ctx.author.display_name}, DazBank has donated {amount} points to {member.display_name}'s' account.", color = 0xffd700)
      em.timestamp = now
      await ctx.send(embed = em)

  @commands.command()
  async def bet(self, ctx, member:discord.Member, amount = None, *arg):
      await self.open_account(ctx.author)
      await self.open_account(member)
      amount = int(amount)
      timezone = pytz.timezone('Australia/Sydney') 
      now = datetime.now(timezone)
      arg = str(arg).replace("(","").replace(")","").replace(",","")
      if amount == None:
          await ctx.send("Please enter the amount of points you'd like to wager")
          return
      bal = await self.update_bank(member)
      if amount>bal:
          await ctx.send(f"{member.display_name} doesn't have that much points")
          return
      if amount<=0:
          await ctx.send("DazBank can only retrieve positive amounts")
          return
      if amount >1000:
          await ctx.send("To avoid developing bad gambling habits, DazBank has limited the bet amount to 999.")
      poll = discord.Embed(title=f"Vote to approve bet result by - {ctx.author.name}#{ctx.author.discriminator}",
                               description=f"**{ctx.author.name}** made the following claim:\n\n **{arg}**\n\nReact with the red stonks if this happened. React with the blue stonks if you do not believe this happened.", colour=discord.Colour.gold())
      poll.add_field(name="Yes", value="📈")
      poll.add_field(name="No", value="📉")
      poll.set_footer(text="Voting ends in 10 seconds.")
      poll_msg = await ctx.send(embed=poll)
      poll_id = poll_msg.id
      await poll_msg.add_reaction("📈") 
      await poll_msg.add_reaction("📉")
      await asyncio.sleep(10)
      poll_msg = await ctx.channel.fetch_message(poll_id)
      votes = {"📈": 0, "📉": 0}
      reacted = []
      for x in poll_msg.reactions:
        if x.emoji in ["📈", "📉"]:
          async for user in x.users():
              votes[x.emoji] += 1
              reacted.append(user.id)
      if votes["📈"] <= votes["📉"]:
        skip = False
        embed = discord.Embed(title="Bet failed", 
                              description=f"*{ctx.author.name} will now be donating {amount} to {member.display_name}.*",
                                  color = 0xffd700)
        await poll_msg.clear_reactions()
        await ctx.send(embed=embed)
      if votes["📈"] > votes["📉"]:
        skip = True
        embed = discord.Embed(title="Bet was successful",
                                          description=f"*{ctx.author.name} will now take {amount} points from {member.display_name}'s account'.*", color = 0xffd700)
        await poll_msg.clear_reactions()
        await ctx.send(embed=embed)
      if not skip:
        await asyncio.sleep(5)
        await self.update_bank(ctx.author, -1*amount, "points")
        await self.update_bank(member, 1*amount, "points")
        await self.update_win(ctx.author, -1*amount, "wins")
        embed = discord.Embed(description = f"DazBank has finished processing {ctx.author.display_name}'s bet.{ctx.author.display_name}'s bet failed and so they have generously donated {amount} points to {member.display_name}'s' account.", color = 0xffd700)
        embed.timestamp = now
        await poll_msg.clear_reactions()
        await ctx.send(embed=embed)
      if skip:
        await asyncio.sleep(5)
        await self.update_bank(ctx.author, 1*amount, "points")
        await self.update_bank(member, -1*amount, "points")
        await self.update_win(ctx.author, 1*amount, "wins")
        embed = discord.Embed(description = f"DazBank has finished processing {ctx.author.display_name}'s bet.{ctx.author.display_name}'s bet was successful and they have taken {amount} points from {member.display_name}'s' account.", color = 0xffd700)
        embed.timestamp = now
        await poll_msg.clear_reactions()
        await ctx.send(embed=embed)
    
  
  @commands.command()
  async def loan(self, ctx, amount):
    user = ctx.author
    amount = int(amount)
    timezone = pytz.timezone('Australia/Sydney') 
    now = datetime.now(timezone)
    await self.open_account(ctx.author)
    users = await self.get_bank_data()
    if amount > 100:
      await ctx.send("DazBank can unfortunately only loan up to 100 points. Request points via !loan x (where x =<100)")
    else:
      users[str(user.id)]["points"] += amount
      users[str(user.id)]["loans"] += amount
      with open("Bank.json", "w") as f:
        json.dump(users,f)
        await ctx.send("DazBank has updated your balance.")
      col = users[str(user.id)]["colour"]
      points_amount = users[str(user.id)]["points"]
      em = discord.Embed(colour =  discord.Colour(int(f"0x{col}", 16)))
      em.set_author(name = f"{ctx.author.display_name}'s updated balance", icon_url=user.avatar_url)
      em.add_field(name = "Points", value = points_amount)
      file = discord.File(".//image//Loan2.jpg", filename="Loan2.jpg")
      em.set_image(url="attachment://Loan2.jpg")
      em.timestamp = now
      await ctx.send(file=file, embed = em)

  @commands.command()
  async def bets_won(self, ctx): 
    Bank_sheet = open('Bank.json')
    json_array = json.load(Bank_sheet)
    manual_ID = []
    manual_wins = []
    for x in json_array:
      manual_ID.append(json_array[x]['ID'])
      manual_wins.append(json_array[x]['wins'])
    leaderboard = dict(zip(manual_ID,manual_wins))
    leaderboard_order=sorted((value, key) for (key,value) in leaderboard.items())
    sort_board= sorted(leaderboard_order, reverse=True)
    sort_board2 = []   
    for x in sort_board:
      x = x[1] + " has won " + str(x[0]) + " points from bets."
      sort_board2.append(x)  
    numbers =[i for i in range(1, len(sort_board2)+1)]
    sort1 = dict(zip(numbers, sort_board2))
    sort = str(sort1).replace(",", "\n").replace("{","").replace("}","").replace("'","")
    pwin = discord.Embed(title = "Leaderboard of points",color = 0xffd700)
    pwin.add_field(name = "list", value = sort)
    file = discord.File(".//image//dunk.jpg", filename="dunk.jpg")
    pwin.set_thumbnail(url="attachment://dunk.jpg")
    await ctx.send(file=file, embed = pwin)
  
  @commands.command()
  async def points_loaned(self, ctx):
    Bank_sheet = open('Bank.json')
    json_array = json.load(Bank_sheet)
    manual_ID = []
    manual_loans = []
    for x in json_array:
      manual_ID.append(json_array[x]['ID'])
      manual_loans.append(json_array[x]['loans'])
    leaderboard = dict(zip(manual_ID,manual_loans))
    leaderboard_order=sorted((value, key) for (key,value) in leaderboard.items())
    sort_board= sorted(leaderboard_order, reverse=True)
    sort_board2 = []   
    for x in sort_board:
      x = x[1] + " has been loaned " + str(x[0]) + " points by DazBank."
      sort_board2.append(x)  
    numbers =[i for i in range(1, len(sort_board2)+1)]
    sort1 = dict(zip(numbers, sort_board2))
    sort = str(sort1).replace(",", "\n").replace("{","").replace("}","").replace("'","")
    loan_amt = discord.Embed(title = "Leaderboard of points",color = 0xffd700)
    loan_amt.add_field(name = "list", value = sort)
    file = discord.File(".//image//bill.jpg", filename="bill.jpg")
    loan_amt.set_thumbnail(url="attachment://bill.jpg")
    await ctx.send(file=file, embed = loan_amt)

  
  @commands.command()
  async def leader(self, ctx): 
    user = ctx.author
    Bank_sheet = open('Bank.json')
    json_array = json.load(Bank_sheet)
    manual_ID = []
    manual_points = []
    for x in json_array:
      manual_ID.append(json_array[x]['ID'])
      manual_points.append(json_array[x]['points'])
    leaderboard = dict(zip(manual_ID,manual_points))
    leaderboard_order=sorted((value, key) for (key,value) in leaderboard.items())
    sort_board= sorted(leaderboard_order, reverse=True)
    sort_board2 = []   
    for x in sort_board:
      x = x[1] + " has " + str(x[0]) + " points"
      sort_board2.append(x)  
    numbers =[i for i in range(1, len(sort_board2)+1)]
    sort1 = dict(zip(numbers, sort_board2))
    sort = str(sort1).replace(",", "\n").replace("{","").replace("}","").replace("'","")
    rank = discord.Embed(title = "Leaderboard of points",color = 0xffd700)
    rank.add_field(name = "list", value = sort)
    file = discord.File(".//image//board.jpg", filename="board.jpg")
    rank.set_thumbnail(url="attachment://board.jpg")
    await ctx.send(file=file, embed = rank)
    

def setup(client):
  client.add_cog(Economy(client))