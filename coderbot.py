import discord
from discord.ext import commands, tasks
import os
import sys
from bot import Bot 
import function as f
import asyncio
import json

# List of Discord IDs for Bot Channels
ID = {
  'epicID': 625041679325462571,
  'statusID': 625049807140159529,
  'commentaryID': 801521814692954153,
  'bottestID': 800872499507101697,
  'archiveID': 801533100588269609,
  'musicID': 801529894899154996,
  'coderbotID': 800867858913165333
}

# Client Spinup
client = discord.Client()

# Asleep Status for Bot Avatar
asleep = discord.Game("State: Asleep")

# Bot Class Intialization
myBot = Bot(client, ID)

@client.event
async def on_ready():
  try: 
    # Epic Coders Guild Object
    epicGuild = client.get_guild(ID['epicID'])

    # CoderBot Member Object
    coderBot = epicGuild.get_member(ID['coderbotID'])

    # Dictionary of Channel Objects
    channels = {
      'status': epicGuild.get_channel(ID['statusID']),
      'commentary': epicGuild.get_channel(ID['commentaryID']),
      'bottest': epicGuild.get_channel(ID['bottestID']),
      'archive': epicGuild.get_channel(ID['archiveID']),
      'music': epicGuild.get_channel(ID['musicID'])
    }

    # Update Asynchronous Information After Client Login
    myBot.updateInformation(channels, epicGuild, coderBot)

    # Success and Bot Starts Up in Sleep State
    print('\n Logged in as: {0.user}\n'.format(client))
    await client.change_presence(activity = asleep)

    # Availability Indicator and Half-Hourly Status Report
    await myBot.channels['status'].send("Hey Everyone! I am alive and sleepy! Wake me up if ya need me OwO!")    
    await myBot.reportStatus()
  
  except Exception as inst:
    _, _, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await myBot.channels['bottest'].send("```" + errorMsg + "```")

@client.event
async def on_message(message):
  try:
    # Kill Switch
    if "!kill" in message.content.lower():
      await myBot.channels['status'].send("Process Killed: Sorry Guys :sob:!")
      await client.logout()

    # If Bot Sends the Message Return !!! DO NOT REMOVE !!!
    if message.author == client.user:
      return

    pack = (myBot, message)
    # Allow Only Sleeping Protocols While Bot is Asleep
    if myBot.asleep:
      result = [await f.sleeping_protocol(*pack)]
      if not myBot.asleep:
        # Process with Other Functions if Bot Wakes up
        result.extend([await f.coin_flip(*pack), await f.roll_dice(*pack), await f.dialogue_handler(*pack), await f.reaction_handler(*pack)])
    else:
      # Process all Functions as Long as Bot is Awake
      result = [await f.sleeping_protocol(*pack), await f.coin_flip(*pack), await f.roll_dice(*pack), await f.dialogue_handler(*pack), await f.reaction_handler(*pack)]

    # Indicates which Functions May Have Had Errors
    if 0 in result:
      raise Exception("Something went wrong: " + str(result))

  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")

@client.event
async def on_error(event, *args, **kwargs):
  # Error Message and Sets Bot to Asleep
  await myBot.channels['status'].send("Oopsies, Sorry Everyone! I'm causing problems :slight_frown:! I'll sleep it off!\n Error Event: " + str(event) + "\n Args: " + str(args) + "\n Kwargs: " + str(kwargs))
  await myBot.oyasumi()
  return

# @client.event
# async def on_typing(channel, user, when):

#   return

@client.event
async def on_message_delete(message):
  # Store Messages in Archive So Everyone Can Have Message Privileges
  await myBot.channels['archive'].send("==================\nMessage Type: Deletion\nAuthor: " + str(f.extract_names(message.author)[0]) + "\nContent: " + str(message.content) + "\n==================")
  return

@client.event
async def on_message_edit(before, after):
  # Store Messages in Archive So Everyone Can Have Message Privileges
  await myBot.channels['archive'].send("==================\nMessage Type: Edit\nAuthor: " + str(f.extract_names(before.author)[0]) + "\nContent (Before): " + str(before.content) + "\nContent (After): " + str(after.content) + "\n==================")
  return

@client.event
async def on_reaction_add(reaction, user):
  await reaction.message.add_reaction(reaction.emoji)
  return

# @client.event
# async def on_disconnect():
#   try:
#     await myBot.channels['status'].send("Sorry Everyone! I'll be back in a bit, having some... technical... difficulties.")
    
#   except Exception as inst:
#     _, _, exc_tb = sys.exc_info()
#     errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
#     await myBot.channels['bottest'].send("```" + errorMsg + "```")
#   return

@client.event
async def on_raw_reaction_remove(payload):
  # print(payload.channel_id, payload.guild_id, payload.member, payload.message_id)
  # reaction = payload.emoji
  # member_self = await client.get_guild(625041679325462571).get_member(800867858913165333)
  # await reaction.message.channel.send("Triggered")
  # print(member_self)
  await reaction.message.remove_reaction(reaction.emoji, myBot.myID)
  return

@client.event
async def on_member_join(member):
  await myBot.channels['commentary'].send("Let Welcome Our New Member Everyone! Everyone say hello to " + str(member.name) + " :partying_face:")
  return

@client.event
async def on_member_remove(member):
  await myBot.channels['commentary'].send("Sorry Everyone, *sniff*, I'm afraid that " + str(member.name) + " has left the server :sob:!")
  return

@client.event
async def on_guild_emojis_update(guild, before, after):
  return

@client.event
async def on_guild_role_update(before, after):
  return

client.run(os.getenv('TOKEN'))
