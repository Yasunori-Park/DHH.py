# -*- coding: utf-8 -*-
#If error 429, run kill 1 in Shell
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import json
import DND_Data as data
import requests


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
    self.char_languages = None
    self.char_order = None
    self.char_role = None
    self.char_species = None
    self.char_weapon = None
    self.char_armour = None
    self.char_strength = None
    self.char_dexterity = None
    self.char_constitution = None
    self.char_hit_die = None
    self.char_hp = None
    self.char_intelligence = None
    self.char_wisdom = None
    self.char_charisma = None
    self.char_status = None
    self.char_ally = None
    self.char_level = None
    self.char_drop = None

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

    #Designate constitution modifier
    if new_character.char_constitution > 11:
      char_con_mod = round((new_character.char_constitution - 10)/2)
    else:
      char_con_mod = 0

    #Assign a hit die
    if new_character.char_role == "Sorcerer" or new_character.char_role == "Wizard":
      new_character.char_hit_die = "d6"
    elif new_character.char_role == "Fighter" or new_character.char_role == "Paladin" or new_character.char_role == "Ranger":
      new_character.char_hit_die = "d10"
    elif new_character.char_role == "Barbarian":
      new_character.char_hit_die = "d12"
    elif new_character.char_role == "Hunting Horner":
      new_character.char_hit_die = "d20"
    else:
      new_character.char_hit_die = "d8"
      
    #HP
    if new_character.char_role == "Sorcerer" or new_character.char_role == "Wizard":
      new_character.char_hp = await self.rolld6(1) + int(char_con_mod)
    elif new_character.char_role == "Fighter" or new_character.char_role == "Paladin" or new_character.char_role == "Ranger":
      new_character.char_hp = char_con_mod + await self.rolld10(1)
    elif new_character.char_role == "Barbarian":
      new_character.char_hp = char_con_mod + await self.rolld12(1)
    elif new_character.char_role == "Hunting Horner":
      new_character.char_hp = char_con_mod + await self.rolld20(1)
    else:
      new_character.char_hp = char_con_mod + await self.rolld8(1)

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

    #Wisdom
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

    #Level for a new character is 1
    new_character.char_level = 1
      
    #Relay character traits and stats
    em = discord.Embed(title = f"{new_character.char_first_name} {new_character.char_last_name}",color = 0xfe0202, description = f"{ctx.author.display_name} has summoned the {new_character.char_species} {new_character.char_role}: {new_character.char_first_name} {new_character.char_last_name}")
    em.add_field(name = f"{new_character.char_first_name} {new_character.char_last_name}'s Sheet", value = f"Status: *{new_character.char_status}*\nSpecies: *{new_character.char_species}*\nClass: *{new_character.char_role}*\nWeapon: *{new_character.char_weapon}*\nArmour: *{new_character.char_armour}*\nOrder: *{new_character.char_order}*\nAge: *{new_character.char_age}*\nHeight (inches): *{new_character.char_height}*\nWeight (pounds): *{new_character.char_weight}*\nSize: *{new_character.char_size}*\nSpeed: *{new_character.char_speed}*\nGender: *{new_character.char_gender}*\nTraits: *{new_character.char_traits}*\nLanguages: *{new_character.char_languages}*")
    em.add_field(name = f"{new_character.char_first_name} {new_character.char_last_name}'s Stats", value = f"Level: *{new_character.char_level}*\nHP: *{new_character.char_hp}*\nHit Dice: *{new_character.char_hit_die}*\nStrength: *{new_character.char_strength}*\nDexterity: *{new_character.char_dexterity}*\nConstitution: *{new_character.char_constitution}*\nIntelligence: *{new_character.char_intelligence}*\nWisdom: *{new_character.char_wisdom}*\nCharisma: *{new_character.char_charisma}*") 
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
    await ctx.channel.send(file=file, embed = em)

    #Store output of class into a json file. Because the new_character is generated on the client side of the Discord client, it is difficult to imagine how to do this in a helper function without manually creating an object everytime. 
    with open("DnD_unit.json", "r") as f:
      unit_ID = json.load(f)
    if str(new_character.char_ID) in unit_ID:
      unit_ID[str(new_character.char_ID)]['first_name']= str(      new_character.char_first_name)
      unit_ID[str(new_character.char_ID)]['last_name']= str(      new_character.char_last_name)
      unit_ID[str(new_character.char_ID)]['status'] = str(new_character.char_status)
      unit_ID[str(new_character.char_ID)]['height'] = str(new_character.char_height)
      unit_ID[str(new_character.char_ID)]['weight'] = str(new_character.char_weight)
      unit_ID[str(new_character.char_ID)]['speed'] = str(new_character.char_speed)
      unit_ID[str(new_character.char_ID)]['traits'] = str(new_character.char_traits)
      unit_ID[str(new_character.char_ID)]['languages'] = str(new_character.char_languages)
      unit_ID[str(new_character.char_ID)]['ally'] = str(new_character.char_ally)
      unit_ID[str(new_character.char_ID)]['gender']= str(      new_character.char_gender)
      unit_ID[str(new_character.char_ID)]['age']= str(      new_character.char_age)
      unit_ID[str(new_character.char_ID)]['order']= str(      new_character.char_order)
      unit_ID[str(new_character.char_ID)]['class']= str(      new_character.char_role)
      unit_ID[str(new_character.char_ID)]['species']= str(      new_character.char_species)
      unit_ID[str(new_character.char_ID)]['weapon']= str(      new_character.char_weapon)
      unit_ID[str(new_character.char_ID)]['armour']= str(      new_character.char_armour)
      unit_ID[str(new_character.char_ID)]['level'] = str(new_character.char_level)
      unit_ID[str(new_character.char_ID)]['hp'] = str(new_character.char_hp)
      unit_ID[str(new_character.char_ID)]['hit dice'] = str(new_character.char_hit_die)
      unit_ID[str(new_character.char_ID)]['strength']= str(      new_character.char_strength)
      unit_ID[str(new_character.char_ID)]['dexterity']= str(      new_character.char_dexterity)
      unit_ID[str(new_character.char_ID)]['constitution']= str(      new_character.char_constitution)
      unit_ID[str(new_character.char_ID)]['intelligence']= str(      new_character.char_intelligence)
      unit_ID[str(new_character.char_ID)]['wisdom']= str(      new_character.char_wisdom)
      unit_ID[str(new_character.char_ID)]['charisma']= str(      new_character.char_charisma)
      unit_ID[str(new_character.char_ID)]['Allegiance']= str(new_character.char_ally)
      unit_ID[str(new_character.char_ID)]['size'] = str(new_character.char_size)
      with open("DnD_unit.json", "w") as f:
        json.dump(unit_ID,f)
    else:
      unit_ID[str(new_character.char_ID)] = {}
      unit_ID[str(new_character.char_ID)]['first_name']= str(      new_character.char_first_name)
      unit_ID[str(new_character.char_ID)]['last_name']= str(      new_character.char_last_name)
      unit_ID[str(new_character.char_ID)]['status'] = str(new_character.char_status)
      unit_ID[str(new_character.char_ID)]['height'] = str(new_character.char_height)
      unit_ID[str(new_character.char_ID)]['weight'] = str(new_character.char_weight)
      unit_ID[str(new_character.char_ID)]['speed'] = str(new_character.char_speed)
      unit_ID[str(new_character.char_ID)]['traits'] = str(new_character.char_traits)
      unit_ID[str(new_character.char_ID)]['languages'] = str(new_character.char_languages)
      unit_ID[str(new_character.char_ID)]['ally'] = str(new_character.char_ally)
      unit_ID[str(new_character.char_ID)]['gender']= str(      new_character.char_gender)
      unit_ID[str(new_character.char_ID)]['age']= str(      new_character.char_age)
      unit_ID[str(new_character.char_ID)]['order']= str(      new_character.char_order)
      unit_ID[str(new_character.char_ID)]['class']= str(      new_character.char_role)
      unit_ID[str(new_character.char_ID)]['species']= str(      new_character.char_species)
      unit_ID[str(new_character.char_ID)]['weapon']= str(      new_character.char_weapon)
      unit_ID[str(new_character.char_ID)]['armour']= str(      new_character.char_armour)
      unit_ID[str(new_character.char_ID)]['level'] = str(new_character.char_level)
      unit_ID[str(new_character.char_ID)]['hp'] = str(new_character.char_hp)
      unit_ID[str(new_character.char_ID)]['hit dice'] = str(new_character.char_hit_die)
      unit_ID[str(new_character.char_ID)]['strength']= str(      new_character.char_strength)
      unit_ID[str(new_character.char_ID)]['dexterity']= str(      new_character.char_dexterity)
      unit_ID[str(new_character.char_ID)]['constitution']= str(      new_character.char_constitution)
      unit_ID[str(new_character.char_ID)]['intelligence']= str(      new_character.char_intelligence)
      unit_ID[str(new_character.char_ID)]['wisdom']= str(      new_character.char_wisdom)
      unit_ID[str(new_character.char_ID)]['charisma']= str(      new_character.char_charisma)
      unit_ID[str(new_character.char_ID)]['allegiance']= str(new_character.char_ally)
      unit_ID[str(new_character.char_ID)]['size'] = str(new_character.char_size)
    with open("DnD_unit.json", "w") as f:
      json.dump(unit_ID,f)


  @commands.command()
  async def passport(self, ctx, user):
    user = str(user)
    if user == "me":
      user = ctx.author.name
    with open("DnD_unit.json", "r") as f:
      unit_ID = json.load(f)
    if user in unit_ID:
      em = discord.Embed(title = unit_ID[str(user)]['first_name'] + " " + unit_ID[str(user)]['last_name'],color = 0xffffff, description = "Details for: " + unit_ID[str(user)]['first_name'] + " " + unit_ID[str(user)]['last_name'])

      em.add_field(name = "{} {}'s sheet".format(unit_ID[str(user)]['first_name'], unit_ID[str(user)]['last_name']), value ="Status: *{}*\nSpecies: *{}*\nClass: *{}*\nWeapon: *{}*\nArmour: *{}*\nOrder: *{}*\nAge: *{}*\nHeight (inches): *{}*\nWeight (pounds): *{}*\nSize: *{}*\nSpeed: *{}*\nGender: *{}*\nTraits: *{}*\nLanguages: *{}*".format(unit_ID[str(user)]['status'], unit_ID[str(user)]['species'], unit_ID[str(user)]['class'], unit_ID[str(user)]['weapon'], unit_ID[str(user)]['armour'], unit_ID[str(user)]['order'], unit_ID[str(user)]['age'] ,unit_ID[str(user)]['height'], unit_ID[str(user)]['weight'], unit_ID[str(user)]['size'], unit_ID[str(user)]['speed'], unit_ID[str(user)]['gender'], unit_ID[str(user)]['traits'], unit_ID[str(user)]['languages']))
      
      em.add_field(name = "{} {}'s stats".format(unit_ID[str(user)]['first_name'], unit_ID[str(user)]['last_name']), value = "Level: *{}*\nHP: *{}*\nHit dice: *{}*\nStrength: *{}*\nDexterity: *{}*\nConstitution: *{}*\nIntelligence: *{}*\nWisdom: *{}*\nCharisma: *{}*".format(unit_ID[str(user)]['level'], unit_ID[str(user)]['hp'], unit_ID[str(user)]['hit dice'], unit_ID[str(user)]['strength'], unit_ID[str(user)]['dexterity'], unit_ID[str(user)]['constitution'], unit_ID[str(user)]['intelligence'], unit_ID[str(user)]['wisdom'], unit_ID[str(user)]['charisma']))
      
      if unit_ID[str(user)]['class'] == "Barbarian":
        file = discord.File(".//DnD_image//Barb.jpg", filename="Barb.jpg")
        em.set_thumbnail(url="attachment://Barb.jpg")
      elif unit_ID[str(user)]['class'] == "Bard":
        file = discord.File(".//DnD_image//Bard.jpg", filename="Bard.jpg")
        em.set_thumbnail(url="attachment://Bard.jpg")
      elif unit_ID[str(user)]['class'] == "Cleric":
        file = discord.File(".//DnD_image//Cleric.jpg", filename="Cleric.jpg")
        em.set_thumbnail(url="attachment://Cleric.jpg")
      elif unit_ID[str(user)]['class'] == "Druid":
        file = discord.File(".//DnD_image//Druid.jpg", filename="Druid.jpg")
        em.set_thumbnail(url="attachment://Druid.jpg")   
      elif unit_ID[str(user)]['class'] == "Fighter":
        file = discord.File(".//DnD_image//Fighter.jpg", filename="Fighter.jpg")
        em.set_thumbnail(url="attachment://Fighter.jpg") 
      elif unit_ID[str(user)]['class'] == "Monk":
        file = discord.File(".//DnD_image//Monk.jpg", filename="Monk.jpg")
        em.set_thumbnail(url="attachment://Monk.jpg")
      elif unit_ID[str(user)]['class'] == "Paladin":
        file = discord.File(".//DnD_image//Palad.jpg", filename="Palad.jpg")
        em.set_thumbnail(url="attachment://Palad.jpg")  
      elif unit_ID[str(user)]['class'] == "Ranger":
        file = discord.File(".//DnD_image//Rang.jpg", filename="Rang.jpg")
        em.set_thumbnail(url="attachment://Rang.jpg") 
      elif unit_ID[str(user)]['class'] == "Rogue":
        file = discord.File(".//DnD_image//Rogue.jpg", filename="Rogue.jpg")
        em.set_thumbnail(url="attachment://Rogue.jpg")
      elif unit_ID[str(user)]['class'] == "Sorcerer":
        file = discord.File(".//DnD_image//Sorc.jpg", filename="Sorc.jpg")
        em.set_thumbnail(url="attachment://Sorc.jpg")
      elif unit_ID[str(user)]['class'] == "Warlock":
        file = discord.File(".//DnD_image//Warl.jpg", filename="Warl.jpg")
        em.set_thumbnail(url="attachment://Warl.jpg")
      elif unit_ID[str(user)]['class'] == "Wizard":
        file = discord.File(".//DnD_image//Wiz.jpg", filename="Wiz.jpg")
        em.set_thumbnail(url="attachment://Wiz.jpg")
      elif unit_ID[str(user)]['class'] == "Hunting Horner":
        file = discord.File(".//DnD_image//Bot.jpg", filename="Bot.jpg")
        em.set_thumbnail(url="attachment://Bot.jpg")
        
      await ctx.channel.send(file=file, embed = em)
    else:
      await ctx.channel.send(f"There is no record of a character assigned to this user. Please make one with the command !NewBlood")

  @commands.command()
  async def rewrite(self, ctx, name, stat, *args):
    new = str(args).replace("(", "").replace("'", "").replace(")", "").replace(",", "")
    stat = str(stat)
    name = str(name)
    with open("DnD_unit.json", "r") as f:
      unit_ID = json.load(f)
    if name in unit_ID:
      if stat not in unit_ID[str(name)]:
        await ctx.channel.send("The stat you want to change appears to be spelt incorrectly. Try the relevant stat in shown in !passport, but in lower case.")
      elif stat == "species" or stat == "age" or stat == "height" or stat == "weight" or stat == "size":
        await ctx.channel.send('"Love Yourself" is a song recorded by Canadian singer Justin Bieber for his fourth studio album *Purpose* (2015). It is also something you should do. Species cannot be changed other than creating a new character via !NewBlood.')
      elif stat == "status":
        if new == "Alive" or new == "Dead" or new == "Afflicted":
          unit_ID[str(name)][stat] = new    
          with open("DnD_unit.json", "w") as f:
            json.dump(unit_ID, f)
          await ctx.channel.send(unit_ID[str(name)]['first_name'] + "'s status is now: " + new + "!")
        else:
          await ctx.channel.send("Invalid status")
      elif stat == "class":
        classes = []
        for _class in data.classes:
          classes.append(_class)
        if new not in classes:
          await ctx.channel.send("Invalid class name")
        else:
          unit_ID[str(name)][stat] = new
          with open("DnD_unit.json", "w") as f:
            json.dump(unit_ID, f)
          await ctx.channel.send(unit_ID[str(name)]['first_name'] + "'s class is now: " + new + "!")
      else:
        unit_ID[str(name)][stat] = new
        with open("DnD_unit.json", "w") as f:
          json.dump(unit_ID, f)
        await ctx.channel.send(unit_ID[str(name)]['first_name'] + "'s " + stat + " is now: " + new + "!")
    else:
      await ctx.channel.send(f"There is no record of a character assigned to this user. Please make one with the command !NewBlood")  
      
  #Due to the setup of the DnD5eapi, it is necessary to check almost every dict whether it first exists, and if it contains any characters or is None 
  @commands.command()
  async def spell(self, ctx, *args):
    spell = str(args).lower().replace(" ", "-").replace("(", "").replace(")", "").replace(",", "").replace("'", "")
    
    DnD_url = "https://www.dnd5eapi.co/api/spells/"
    final_url = DnD_url + spell
    response = requests.get(final_url)
    json_data = json.loads(response.text)

    name = json_data['name']

    desc = json_data['desc']
    desc = " ".join(desc)
    
    if 'higher_level' in json_data and json_data['higher_level']:
      higher_level = json_data['higher_level']
    else:
      higher_level = "Not applicable"

    if 'range' in json_data and json_data['range']:
      range = json_data['range']
    else:
      range = "Not applicable"

    if 'components' in json_data and json_data['components']:
      components = json_data['components']
      components = " ".join(components).replace("V", "Verbal").replace("S", "Somatic").replace("M", "Material").replace(" ", ", ")
    else:
      components = "Not applicable"

    if 'material' in json_data and json_data['material']:
      material = json_data['material']
    else:
      material = "Not applicable"

    if 'ritual' in json_data and json_data['ritual']:
      ritual = json_data['ritual']
    else:
      ritual = "Not applicable"

    if 'duration' in json_data and json_data['duration']:
      duration = json_data['duration']   
    else:
      duration = "Not applicable"

    if 'concentration' in json_data and json_data['concentration']:
      concentration = json_data['concentration']
    else:
      concentration = "Not applicable"

    if 'cast_time' in json_data and json_data['cast_time']:
      cast_time = json_data['casting_time'] 
    else:
      cast_time = "Not applicable"
    
    if 'level' in json_data and json_data['level']:
      level = json_data['level']
    else:
      level = "Not applicable"

    if "heal_at_slot_level" in json_data and json_data['heal_at_slot_level']:
      heal_slot = json_data['heal_at_slot_level']
      heal_slot = str(heal_slot).replace("{", "").replace("}", "").replace(", ", "\n")
    else:
      heal_slot = "Not applicable"

    if 'attack_type' in json_data and json_data['attack_type']:
      atk_type = json_data['attack_type']
    else:
      atk_type = "Not applicable"

    if 'damage' in json_data and json_data['damage']:
      dmg_type = json_data['damage']['damage_type']['name']
      if 'damage_at_slot_level' in json_data['damage'] and json_data['damage']['damage_at_slot_level']:
        dmg_slot = json_data['damage']['damage_at_slot_level']
        dmg_slot = str(dmg_slot).replace(", ", "\n").replace("{", "").replace("}", "")
      else:
        dmg_slot = "Not applicable"
      if 'damage_at_character_level' in json_data['damage'] and json_data['damage']['damage_at_character_level']:
        dmg_char = json_data['damage_at_character_level']
        dmg_char = str(dmg_char).replace(", ", "\n").replace("{", "").replace("}", "")
      else:
        dmg_char = "Not applicable"
    else:
      dmg_type = "Not applicable"

    if 'dc' in json_data and json_data['dc']:
      if 'dc_success' in json_data['dc']['dc_type'] and json_data['dc']['dc_type']['dc_success']:
        dc_scs = json_data['dc']['dc_type']['dc_success']
      else:
        dc_scs = "Not applicable" 
      if 'dc_type' in json_data['dc'] and json_data['dc']['dc_type']:
        dc_type = json_data['dc']['dc_type']['name']
      else:
        dc_type = "Not applicable"
      if 'desc' in json_data['dc']['dc_type'] and json_data['dc']['dc_type']['desc']:
        dc_desc = json_data['dc']['dc_type']['desc']
      else:
        dc_desc = "Not applicable"

    if 'area_of_effect' in json_data and json_data['area_of_effect']:
      AOE = json_data['area_of_effect']
      AOE = str(AOE).replace("{", "").replace("}", "").replace(", ", "\n")
    else:
      AOE = "Not applicable"

    if 'school' in json_data and json_data['school']:
      school = json_data['school']['name']
    else:
      school = "Not applicable"

    if 'classes' in json_data and json_data['classes']:
      roles = [i['name'] for i in json_data['classes']]
      roles = str(roles).replace("[", "").replace("'", "").replace("]", "")
    else:
      roles = "Not applicable"

    em = discord.Embed(title = "testing",color = 0x8b008b, description = "Details for: ")

    em.add_field(name = "Spell details", value = "xyz")
#Test all variables are working for examples: shield of faith, thunderwave, curses, healing spells
    await ctx.channel.send(desc)


  @commands.command()
  async def summon_pandora(self, ctx):
    pandora = Character(self)

    #Assign a unique ID so if character name ever changes a reference exists
    pandora.char_ID == "Pandora"

    #Assign a gender
    gender = []
    for _gender in data.gender:
      gender.append(_gender)
    pandora.char_gender = gender[random.randrange(0, len(gender))]
    
    #Assign a name which will simply be a title + a merge of two species
    title = []
    for _title in data.mon_title:
      title.append(_title)
    pandora.char_first_name = title[random.randrange(0, len(title))]
    
    species = []
    for _species in data.mon_species:
      species.append(_species)
    pandora.char_last_name = species[random.randrange(0, len(species))]
        
    #Assign a weapon for the monster
    weapon = []
    for _weapon in data.mon_weapon:
      weapon.append(_weapon)
    pandora.char_weapon=weapon[random.randrange(0, len(weapon))]
    
    #Assign armour for the monster
    armour = []
    for _arm in data.mon_armour:
      armour.append(_arm)
    pandora.char_armour = armour[random.randrange(0, len(armour))]

    #Assign stats
    pandora.char_wisdom = random.randint(20, 40)
    pandora.char_strength = random.randint(20, 90)
    pandora.char_dexterity = random.randint(1, 5)
    pandora.char_constitution = random.randint(1, 5)
    pandora.char_intelligence = random.randint(20, 40)
    pandora.char_charisma = random.randint(20, 40)
    pandora.char_hp = random.randint(40, 100)
    pandora.char_level = random.randint(10, 999)
    pandora.char_age = random.randint(1, 400)
    size = ["Microscopic", "Small", "Medium", "Large", "Colossal"]
    pandora.char_size = size[random.randrange(0, len(size))]
    if pandora.char_size == "Microscopic":
      pandora.char_height = random.randint(1, 5)
      pandora.char_speed = random.randint(1, 2)
    elif pandora.char_size == "Small":
      pandora.char_height = random.randint(5, 90)
      pandora.char_speed = random.randint(2, 10)
    elif pandora.char_size == "Medium":
      pandora.char_height = random.randint(90, 180)
      pandora.char_speed = random.randint(10, 21)
    elif pandora.char_size == "Large":
      pandora.char_height = random.randint(180, 1500)
      pandora.char_speed = random.randint(21, 100)
    else:
      pandora.char_height = random.randint(1500, 14000)
      pandora.char_speed = random.randint(100, 200)
    pandora.char_weight = random.randint(1, 9999)

    #Assign traits

    #Assign languages

    #Assign as enemy
    pandora.char_status = "Enemy"
    pandora.char_ally = "Not"

    #Assign rewards
    exp = random.randint(0, 200)
    reward = []
    for _reward in data.mon_drop:
      reward.append(_reward)
    drop = reward[random.randrange(0, len(reward))]
    pandora.char_drop = "By defeating the beast from Pandora's magical orb, the party earns:\nExp.: " + str(exp) + "\nEquipment: " + str(drop) 
    
    with open("DnD_unit.json", "r") as f:
      unit_ID = json.load(f)
    if str(pandora.char_ID) in unit_ID:
      unit_ID[str(pandora.char_ID)]['first_name']= str(      pandora.char_first_name)
      unit_ID[str(pandora.char_ID)]['last_name']= str(      pandora.char_last_name)
      unit_ID[str(pandora.char_ID)]['status'] = str(pandora.char_status)
      unit_ID[str(pandora.char_ID)]['height'] = str(pandora.char_height)
      unit_ID[str(pandora.char_ID)]['weight'] = str(pandora.char_weight)
      unit_ID[str(pandora.char_ID)]['speed'] = str(pandora.char_speed)
      unit_ID[str(pandora.char_ID)]['traits'] = str(pandora.char_traits)
      unit_ID[str(pandora.char_ID)]['languages'] = str(pandora.char_languages)
      unit_ID[str(pandora.char_ID)]['ally'] = str(pandora.char_ally)
      unit_ID[str(pandora.char_ID)]['gender']= str(      pandora.char_gender)
      unit_ID[str(pandora.char_ID)]['weapon']= str(      pandora.char_weapon)
      unit_ID[str(pandora.char_ID)]['armour']= str(      pandora.char_armour)
      unit_ID[str(pandora.char_ID)]['level'] = str(pandora.char_level)
      unit_ID[str(pandora.char_ID)]['hp'] = str(pandora.char_hp)
      unit_ID[str(pandora.char_ID)]['strength']= str(      pandora.char_strength)
      unit_ID[str(pandora.char_ID)]['dexterity']= str(      pandora.char_dexterity)
      unit_ID[str(pandora.char_ID)]['constitution']= str(      pandora.char_constitution)
      unit_ID[str(pandora.char_ID)]['intelligence']= str(      pandora.char_intelligence)
      unit_ID[str(pandora.char_ID)]['wisdom']= str(      pandora.char_wisdom)
      unit_ID[str(pandora.char_ID)]['charisma']= str(      pandora.char_charisma)
      unit_ID[str(pandora.char_ID)]['size'] = str(pandora.char_size)
      with open("DnD_unit.json", "w") as f:
        json.dump(unit_ID,f)




def setup(client):
  client.add_cog(Character(client))
