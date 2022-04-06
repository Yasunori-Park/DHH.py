# -*- coding: utf-8 -*-
#If error 429, run kill 1 in Shell
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import Daz_activity as D
import random
import json
import DND_Data as data


client = discord.Client()
client = commands.Bot(command_prefix='!')
client.remove_command("help")
intents = discord.Intents.default()
intents.members = True

#Class for DND
class Character(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.char_ID = None
    self.char_first_name = None
    self.char_last_name = None
    self.char_gender = None
    self.char_age = None
    self.char_height = None
    self.char_weight = None
    self.char_size = None
    self.char_speed = None
    self.char_traits = None
    self.char_language = None
    self.char_order = None
    self.char_role = None
    self.char_species = None
    self.char_weapon = None
    self.char_armour = None
    self.char_strength = None
    self.char_dexterity = None
    self.char_constitution = None
    self.char_intelligence = None
    self.char_wisdom = None
    self.char_charisma = None
    self.char_status = None
    self.char_ally = None

  async def rolld4(self, x):
    x= int(x)
    d4 = []
    total = 0
    for i in range(x):
      d4.append(random.randrange(1,5))
    for x in d4:
      total += x
    return total

  async def rolld6(self, x):
    x= int(x)
    d6 = []
    total = 0
    for i in range(x):
      d6.append(random.randrange(1,7))
    for x in d6:
      total += x
    return total

  async def rolld8(self, x):
    x= int(x)
    d8 = []
    total = 0
    for i in range(x):
      d8.append(random.randrange(1,9))
    for x in d8:
      total += x
    return total

  async def rolld10(self, x):
    x= int(x)
    d10 = []
    total = 0
    for i in range(x):
      d10.append(random.randrange(1,11))
    for x in d10:
      total += x
    return total

  async def rolld12(self, x):
    x= int(x)
    d12 = []
    total = 0
    for i in range(x):
      d12.append(random.randrange(1,13))
    for x in d12:
      total += x
    return total

  async def rolld20(self, x):
    x = int(x)
    d20 = []
    total = 0
    for i in range(x):
      d20.append(random.randrange(1, 21))
    for x in d20:
      total += x
    return total

  async def rolld6_stats(self, x):
    x= int(x)
    d6 = []
    for i in range(x):
      d6.append(random.randrange(1,7))
    total = 0
    lowest = d6[0]
    for x in d6:
      total += x
    for x in d6:
      if x < lowest:
        x = lowest
    return total - lowest
  
  async def rolld20_stats(self, x):
    x= int(x)
    d20 = []
    for i in range(x):
      d20.append(random.randrange(1,21))
    total = 0
    lowest = d20[0]
    for x in d20:
      total += x
    for x in d20:
      if x < lowest:
        x = lowest
    return total - lowest

  @commands.command()
  async def roll(self, ctx, x, y):
    x = int(x)
    x2 = x + 1
    y = int(y)
    dice = []
    results = []
    total = 0
    for i in range(y):
      dice.append(random.randrange(1, x2))
    for rolls in dice:
      results.append(rolls)
      total += rolls
    results = str(results).replace("[","").replace("]","").replace(","," ")
    await ctx.channel.send(f"{ctx.author.display_name} rolled a " + str(x) + " sided die " + str(y) + " times!\nThe result is:  " + str(results) + "\nThese rolls adds up to: " + str(total))
    
  @commands.command()
  async def NewBlood(self, ctx):
    new_character = Character(self)

    #Assign a unique ID so if character name ever changes a reference exists
    new_character.char_ID = ctx.author.name
    
    #Assign a class
    classes = []
    for _class in data.classes:
      classes.append(_class)
    new_character.char_role = classes[random.randrange(0, len(classes))]
    
    #Assign a race
    species = []
    for _race in data.races:
      species.append(_race)
    new_character.char_species= species[random.randrange(0, len(species))]

    #Assign a gender
    gender = []
    for _gender in data.gender:
      gender.append(_gender)
    new_character.char_gender = gender[random.randrange(0, len(gender))]
    
    #Assign an order
    order = []
    for _order in data.dieties:
      order.append(_order)
    new_character.char_order = order[random.randrange(0, len(order))]
    
    #Assign a first name
    fname = []
    #Half-Elves can be named under both Human or Elf. Merge human and elf first names into one and then allow rand. selection if species == Half-Elf
    if new_character.char_gender == "male":
      if new_character.char_species == 'Half-Elf':
        he_names = []
        for _fname in data.races['Human']['m first names']:
          he_names.append(_fname)
        for _fname in data.races['Elf']['m first names']:
          he_names.append(_fname)
          fname = he_names[random.randrange(0, len(he_names))]
          new_character.char_first_name = fname
      else: 
        for _fname in data.races[new_character.char_species]['m first names']:
          fname.append(_fname)
          new_character.char_first_name = fname[random.randrange(0, len(fname))]
          
    if new_character.char_gender == "female":
      if new_character.char_species == 'Half-Elf':
        he_names = []
        for _fname in data.races['Human']['f first names']:
          he_names.append(_fname)
        for _fname in data.races['Elf']['f first names']:
          he_names.append(_fname)
          fname = he_names[random.randrange(0, len(he_names))]
          new_character.char_first_name = fname
      else:
        for _fname in data.races[new_character.char_species]['f first names']:
          fname.append(_fname)
          new_character.char_first_name = fname[random.randrange(0, len(fname))]

    if new_character.char_gender == "non-binary":
      if new_character.char_species == 'Half-Elf':
        he_names = []
        for _fname in data.races['Human']['m first names']:
          he_names.append(_fname)
        for _fname in data.races['Human']['f first names']:
          he_names.append(_fname)
        for _fname in data.races['Elf']['m first names']:
          he_names.append(_fname)
        for _fname in data.races['Elf']['f first names']:
          he_names.append(_fname)
          fname = he_names[random.randrange(0, len('first names'))]
          new_character.char_first_name = fname
      else: 
        for _fname in data.races[new_character.char_species]['m first names']:
          fname.append(_fname)
        for _fname in data.races[new_character.char_species]['f first names']:
          fname.append(_fname)
          new_character.char_first_name = fname[random.randrange(0, len(fname))]
        
    #Assign a last name
    lname = []
    if new_character.char_species == 'Half-Elf':
      he_lnames = []
      for _lname in data.races['Human']['last names']:
        he_lnames.append(_lname)
      for _lname in data.races['Human']['last names']:
        he_lnames.append(_lname)
        lname = he_lnames[random.randrange(0, len('last names'))]
        new_character.char_last_name = lname
    else:
      for _lname in data.races[new_character.char_species]['last names']:
        lname.append(_lname)
        new_character.char_last_name = lname[random.randrange(0, len(lname))]
        
    #Assign a weapon
    weapon = []
    for _weapon in data.classes[new_character.char_role]['weapons']:
      weapon.append(_weapon)
    new_character.char_weapon=weapon[random.randrange(0, len(weapon))]
    
    #Assign armour
    armour = []
    for _arm in data.classes[new_character.char_role]['armor']:
      armour.append(_arm)
    new_character.char_armour = armour[random.randrange(0, len(armour))]

    #Assign age
    if new_character.char_species == "Human":
      new_character.char_age = await self.rolld4(5) + 15
    elif new_character.char_species == "Elf":
      new_character.char_age = await self.rolld6(6) + 110
    elif new_character.char_species == "Gnome":
      new_character.char_age = await self.rolld6(6) + 40
    elif new_character.char_species == "Halfling":
      new_character.char_age = await self.rolld6(3) + 20
    elif new_character.char_species == "Dwarf":
      new_character.char_age = await self.rolld6(5) + 40
    elif new_character.char_species == "Half-Elf":
      new_character.char_age = await self.rolld6(2) + 20
    elif new_character.char_species == "Half-Orc":
      new_character.char_age = await self.rolld6(1) + 14
    elif new_character.char_species == "Dragonborn":
      new_character.char_age = await self.rolld6(1) + 20
    elif new_character.char_species == "Tiefling":
      new_character.char_age = await self.rolld6(1) + 15
    elif new_character.char_species == "Daz":
      new_character.char_age = str(data.races['Daz']['age'])


    #Assign height
    if new_character.char_species == "Human":
      new_character.char_height = await self.rolld4(2) + 58
    elif new_character.char_species == "Elf":
      new_character.char_height = await self.rolld6(2) + 58
    elif new_character.char_species == "Gnome":
      new_character.char_height = await self.rolld4(2) + 36
    elif new_character.char_species == "Halfling":
      new_character.char_height = await self.rolld4(2) + 32
    elif new_character.char_species == "Dwarf":
      new_character.char_height = await self.rolld4(2) + 45
    elif new_character.char_species == "Half-Elf":
      new_character.char_height = await self.rolld8(2) + 55
    elif new_character.char_species == "Half-Orc":
      new_character.char_height = await self.rolld12(2) + 58
    elif new_character.char_species == "Dragonborn":
      new_character.char_height = await self.rolld8(2) + 190
    elif new_character.char_species == "Tiefling":
      new_character.char_height = await self.rolld8(2)+ 180
    elif new_character.char_species == "Daz":
      new_character.char_height = await self.rolld20(2) + 9999

    #Assign weight
    if new_character.char_species == "Human":
      new_character.char_weight = await self.rolld6(2) + 120
    elif new_character.char_species == "Elf":
      new_character.char_weight = await self.rolld6(1) + 85
    elif new_character.char_species == "Gnome":
      new_character.char_weight = await self.rolld6(1) + 40
    elif new_character.char_species == "Halfling":
      new_character.char_weight = await self.rolld4(1) + 30
    elif new_character.char_species == "Dwarf":
      new_character.char_weight = await self.rolld6(2) + 130
    elif new_character.char_species == "Half-Elf":
      new_character.char_weight = await self.rolld4(2) + 100
    elif new_character.char_species == "Half-Orc":
      new_character.char_weight = await self.rolld6(2) + 150
    elif new_character.char_species == "Dragonborn":
      new_character.char_weight = await self.rolld6(2) + 220
    elif new_character.char_species == "Tiefling":
      new_character.char_weight = await self.rolld6(2)+ 150
    elif new_character.char_species == "Daz":
      new_character.char_weight = await self.rolld20(2) + 9999

    #Assign size, speed, traits and languages
    new_character.char_size = data.races[new_character.char_species]['size']
    new_character.char_speed = data.races[new_character.char_species]['speed']
    new_character.char_traits = str(data.races[new_character.char_species]['traits']).replace("[","").replace("]","").replace("'", "")
    new_character.char_languages = str(data.races[new_character.char_species]['languages']).replace("[","").replace("]","").replace("'", "")

    
    #Strength
    if new_character.char_species == "Human":
      new_character.char_strength = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Half-Orc":
      new_character.char_strength = await self.rolld6_stats(4) + 2
    elif new_character.char_species == "Dwarf":
      new_character.char_strength = await self.rolld6_stats(4) + 2
    elif new_character.char_species == "Dragonborn":
      new_character.char_strength = await self.rolld6_stats(4) + 2
    elif new_character.char_species == "Daz":
      new_character.char_strength = await self.rolld20_stats(4) + 900
    else:
      new_character.char_strength = await self.rolld6_stats(4)

    #Dexterity
    if new_character.char_species == "Human":
      new_character.char_dexterity = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Elf":
      new_character.char_dexterity = await self.rolld6_stats(4) + 2
    elif new_character.char_species == "Halfling":
      new_character.char_dexterity = await self.rolld6_stats(4) + 2
    elif new_character.char_species == "Gnome":
      new_character.char_dexterity = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Daz":
      new_character.char_dexterity = await self.rolld20_stats(4) + 900
    else: 
      new_character.char_dexterity = await self.rolld6_stats(4)

    #Constitution
    if new_character.char_species == "Human":
      new_character.char_constitution = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Dwarf":
      new_character.char_constitution = await self.rolld6_stats(4) + 2 
    elif new_character.char_species == "Half-Orc":
      new_character.char_constitution = await self.rolld6_stats(4) + 1 
    elif new_character.char_species == "Halfling":
      new_character.char_constitution = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Gnome":
      new_character.char_constitution = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Daz":
      new_character.char_constitution = await self.rolld20_stats(4) + 900
    else:
      new_character.char_constitution = await self.rolld6_stats(4)

    #Intelligence
    if new_character.char_species == "Human":
      new_character.char_intelligence = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Tiefling":
      new_character.char_intelligence = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Elf":
      new_character.char_intelligence = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Gnome":
      new_character.char_intelligence = await self.rolld6_stats(4) + 2
    elif new_character.char_species == "Daz":
      new_character.char_intelligence = await self.rolld20_stats(4) + 900
    else: 
      new_character.char_intelligence = await self.rolld6_stats(4)

    #Wisdom - Human wisdom does not work for some reason
    if new_character.char_species == "Human":
      new_character.char_wisdom = await self.rolld6_stats(4) + 1
    if new_character.char_species == "Dwarf":
      new_character.char_wisdom = await self.rolld6_stats(4) + 1
    if new_character.char_species == "Elf":
      new_character.char_wisdom = await self.rolld6_stats(4) + 1
    if new_character.char_species == "Daz":
      new_character.char_wisdom = await self.rolld20_stats(4) + 900
    else:
      new_character.char_wisdom = await self.rolld6_stats(4)

    #Charisma
    if new_character.char_species == "Human":
      new_character.char_charisma = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Dragonborn":
      new_character.char_charisma = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Halfling":
      new_character.char_charisma = await self.rolld6_stats(4) + 1
    elif new_character.char_species == "Half-Elf":
      new_character.char_charisma = await self.rolld6_stats(4) + 2
    elif new_character.char_species == "Tiefling":
      new_character.char_charisma = await self.rolld6_stats(4) + 2  
    elif new_character.char_species == "Daz":
      new_character.char_charisma = await self.rolld20_stats(4) + 900
    else:
      new_character.char_charisma = await self.rolld6_stats(4)

    #Status + Ally (designate as NOT enemy)
    new_character.char_status = "Alive"
    new_character.char_ally = "Party"
      
    #Relay character traits and stats
    em = discord.Embed(title = f"{new_character.char_first_name} {new_character.char_last_name}",color = 0xfe0202, description = f"{ctx.author.display_name} has summoned the {new_character.char_species} {new_character.char_role}: {new_character.char_first_name} {new_character.char_last_name}")
    em.add_field(name = f"{new_character.char_first_name} {new_character.char_last_name}'s Sheet", value = f"Status: *{new_character.char_status}*\nSpecies: *{new_character.char_species}*\nClass: *{new_character.char_role}*\nWeapon: *{new_character.char_weapon}*\nArmour: *{new_character.char_armour}*\nOrder: *{new_character.char_order}*\nAge: *{new_character.char_age}*\nHeight (inches): *{new_character.char_height}*\nWeight (pounds): *{new_character.char_weight}*\nSize: *{new_character.char_size}*\nSpeed: *{new_character.char_speed}*\nGender: *{new_character.char_gender}*\nTraits: *{new_character.char_traits}*\nLanguages: *{new_character.char_languages}*")
    em.add_field(name = f"{new_character.char_first_name} {new_character.char_last_name}'s Stats", value = f"Strength: *{new_character.char_strength}*\nDexterity: *{new_character.char_dexterity}*\nConstitution: *{new_character.char_constitution}*\nIntelligence: *{new_character.char_intelligence}*\nWisdom: *{new_character.char_wisdom}*\nCharisma: *{new_character.char_charisma}*") 
    if new_character.char_role == "Barbarian":
      file = discord.File(".//DnD_image//Barb.jpg", filename="Barb.jpg")
      em.set_thumbnail(url="attachment://Barb.jpg")
    elif new_character.char_role == "Bard":
      file = discord.File(".//DnD_image//Bard.jpg", filename="Bard.jpg")
      em.set_thumbnail(url="attachment://Bard.jpg")
    elif new_character.char_role == "Cleric":
      file = discord.File(".//DnD_image//Cleric.jpg", filename="Cleric.jpg")
      em.set_thumbnail(url="attachment://Cleric.jpg")
    elif new_character.char_role == "Druid":
      file = discord.File(".//DnD_image//Druid.jpg", filename="Druid.jpg")
      em.set_thumbnail(url="attachment://Druid.jpg")   
    elif new_character.char_role == "Fighter":
      file = discord.File(".//DnD_image//Fighter.jpg", filename="Fighter.jpg")
      em.set_thumbnail(url="attachment://Fighter.jpg") 
    elif new_character.char_role == "Monk":
      file = discord.File(".//DnD_image//Monk.jpg", filename="Monk.jpg")
      em.set_thumbnail(url="attachment://Monk.jpg")
    elif new_character.char_role == "Paladin":
      file = discord.File(".//DnD_image//Palad.jpg", filename="Palad.jpg")
      em.set_thumbnail(url="attachment://Palad.jpg")  
    elif new_character.char_role == "Ranger":
      file = discord.File(".//DnD_image//Rang.jpg", filename="Rang.jpg")
      em.set_thumbnail(url="attachment://Rang.jpg") 
    elif new_character.char_role == "Rogue":
      file = discord.File(".//DnD_image//Rogue.jpg", filename="Rogue.jpg")
      em.set_thumbnail(url="attachment://Rogue.jpg")
    elif new_character.char_role == "Sorcerer":
      file = discord.File(".//DnD_image//Sorc.jpg", filename="Sorc.jpg")
      em.set_thumbnail(url="attachment://Sorc.jpg")
    elif new_character.char_role == "Warlock":
      file = discord.File(".//DnD_image//Warl.jpg", filename="Warl.jpg")
      em.set_thumbnail(url="attachment://Warl.jpg")
    elif new_character.char_role == "Wizard":
      file = discord.File(".//DnD_image//Wiz.jpg", filename="Wiz.jpg")
      em.set_thumbnail(url="attachment://Wiz.jpg")
    elif new_character.char_role == "Hunting Horner":
      file = discord.File(".//DnD_image//Bot.jpg", filename="Bot.jpg")
      em.set_thumbnail(url="attachment://Bot.jpg")
    await ctx.send(file=file, embed = em)

    #Store output of class into a json file. Because the new_character is generated on the client side of the Discord client, it is difficult to imagine how to do this in a helper function without manually creating an object everytime. 
    with open("DND_unit.json", "r") as f:
      unit_ID = json.load(f)
    if str(new_character.char_ID) in unit_ID:
      unit_ID[str(new_character.char_ID)]['first name']= str(      new_character.char_first_name)
      unit_ID[str(new_character.char_ID)]['last name']= str(      new_character.char_last_name)
      unit_ID[str(new_character.char_ID)]['gender']= str(      new_character.char_gender)
      unit_ID[str(new_character.char_ID)]['age']= str(      new_character.char_age)
      unit_ID[str(new_character.char_ID)]['order']= str(      new_character.char_order)
      unit_ID[str(new_character.char_ID)]['class']= str(      new_character.char_role)
      unit_ID[str(new_character.char_ID)]['species']= str(      new_character.char_species)
      unit_ID[str(new_character.char_ID)]['weapon']= str(      new_character.char_weapon)
      unit_ID[str(new_character.char_ID)]['armour']= str(      new_character.char_armour)
      unit_ID[str(new_character.char_ID)]['strength']= str(      new_character.char_strength)
      unit_ID[str(new_character.char_ID)]['dexterity']= str(      new_character.char_dexterity)
      unit_ID[str(new_character.char_ID)]['constitution']= str(      new_character.char_constitution)
      unit_ID[str(new_character.char_ID)]['intelligence']= str(      new_character.char_intelligence)
      unit_ID[str(new_character.char_ID)]['wisdom']= str(      new_character.char_wisdom)
      unit_ID[str(new_character.char_ID)]['charisma']= str(      new_character.char_charisma)
      unit_ID[str(new_character.char_ID)]['Allegiance']= str(new_character.char_ally)
      with open("DND_unit.json", "w") as f:
        json.dump(unit_ID,f)
    else:
      unit_ID[str(new_character.char_ID)] = {}
      unit_ID[str(new_character.char_ID)]['first name']= str(      new_character.char_first_name)
      unit_ID[str(new_character.char_ID)]['last name']= str(      new_character.char_last_name)
      unit_ID[str(new_character.char_ID)]['gender']= str(      new_character.char_gender)
      unit_ID[str(new_character.char_ID)]['age']= str(      new_character.char_age)
      unit_ID[str(new_character.char_ID)]['order']= str(      new_character.char_order)
      unit_ID[str(new_character.char_ID)]['class']= str(      new_character.char_role)
      unit_ID[str(new_character.char_ID)]['species']= str(      new_character.char_species)
      unit_ID[str(new_character.char_ID)]['weapon']= str(      new_character.char_weapon)
      unit_ID[str(new_character.char_ID)]['armour']= str(      new_character.char_armour)
      unit_ID[str(new_character.char_ID)]['strength']= str(      new_character.char_strength)
      unit_ID[str(new_character.char_ID)]['dexterity']= str(      new_character.char_dexterity)
      unit_ID[str(new_character.char_ID)]['constitution']= str(      new_character.char_constitution)
      unit_ID[str(new_character.char_ID)]['intelligence']= str(      new_character.char_intelligence)
      unit_ID[str(new_character.char_ID)]['wisdom']= str(      new_character.char_wisdom)
      unit_ID[str(new_character.char_ID)]['charisma']= str(      new_character.char_charisma)
      unit_ID[str(new_character.char_ID)]['Allegiance']= str(new_character.char_ally)
    with open("DND_unit.json", "w") as f:
      json.dump(unit_ID,f)



def setup(client):
  client.add_cog(Character(client))
