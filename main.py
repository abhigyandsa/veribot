import pandas as pd
import discord
import os
import re
from dotenv import load_dotenv
load_dotenv()


def getData(filename, colid):
  sheet = pd.read_excel(filename)
  sheet = sheet.sort_values(colid)
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
    if binsearch(id, idlst) != -1:
        role = discord.utils.get(message.guild.roles, name=role)
        await member.add_roles(role)
        await message.reply('You are now verified!')
    else:
        await message.reply('Sorry! Your ID('+id+') does not match our records.')




async def usage(message):
    await message.reply('This bot helps you get verified!\nUsage: ```$verify 21fxxxxxxx```')

if __name__ == "__main__":
  filename = "names.xlsx"
  idlst = getData(filename, "ID")
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
