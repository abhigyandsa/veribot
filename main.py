import pandas as pd # if this fails, install pandas: pip install pandas
import discord # if this fails, install discord: pip install discord
import os
import random
import re
from dotenv import load_dotenv # if this fails, install dotenv: pip install dotenv
load_dotenv()

def getData(filename,sortid, colid):
  sheet = pd.read_excel(filename)
  sheet = sheet.sort_values(sortid)
  lst = list(sheet[colid])
  del sheet
  return lst

def binsearch(item, list):
    item = item.upper()
    low = 0
    high = len(list) - 1
    while low <= high:
        mid = (low+high) // 2
        if list[mid] == item:
            return mid
        elif list[mid] < item:
            low = mid + 1
        else: 
            high = mid - 1
    return -1

async def createrole(message, role, color=None):
    roles = [ x.name for x in message.author.guild.roles ]
    if role in roles:
        return
    if color:
        await message.author.guild.create_role(name=role, color=color)
    else:
        await message.author.guild.create_role(name=role)


async def verify(message, role):
    roles = [ x.name for x in message.author.roles ]
    if role in roles:
        await message.reply('You are already verified. Cheers!')
        return
    msgstr = message.content
    msglow = msgstr.lower()
    match = re.search('21f.......', msglow)
    if match == None:
        await usage(message)
        return
    member = message.author
    id = match.group()
    index = binsearch(id, idlst)
    if index != -1:
        # creating role verified and assigning it to user
        await createrole(message, role)
        role = discord.utils.get(message.guild.roles, name=role)
        await member.add_roles(role)

        # creating role for group id and assigning it to user
        grpid = 'Group ' + str(gridlst[index])
        random.seed(grpid)
        rancolr = random.randint(0x000000, 0xffffff)
        await createrole(message, grpid, rancolr)
        grprole = discord.utils.get(message.guild.roles, name=grpid)
        await member.add_roles(grprole)

        await message.reply('You are now verified!')
    else:
        await message.reply('Sorry! Your ID('+id+') does not match our records.')

async def usage(message):
    await message.reply('This bot helps you get verified!\nUsage: ```$verify 21fxxxxxxx```')

if __name__ == "__main__":
  filename = "names.xlsx"
  idlst = getData(filename, "ID", "ID")
  gridlst = getData(filename, "ID", "GRID")
  client = discord.Client()
  role = os.getenv('ROLE')

  @client.event
  async def on_ready():
      print('We have logged in as {0.user}'.format(client))

  @client.event
  async def on_message(message):
    if message.author == client.user: 
          return
    msgstr = message.content
    msglow = msgstr.lower()
    if msglow.startswith('$hel'):
        await usage(message)
    if msglow.startswith('$verify'):
        await verify(message, role)
  client.run(os.getenv('VERIBOTTOKEN'))
