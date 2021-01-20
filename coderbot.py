import discord
import os
import sys
from bot import Bot 
import function as f
import asyncio
import schedule

client = discord.Client()
asleep = discord.Game("State: Asleep")
myBot = Bot(client)

@client.event
async def on_ready():
  try: 
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity = asleep)
    schedule.every().hour.at(":00").do(f.reportStatus(myBot))
    for guild in client.guilds:
      await guild.get_channel(625049807140159529).send("Hey Everyone! I am up and sleepy, wake me up if ya need me OwO!")

  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    for guild in client.guilds:
        await guild.get_channel(800872499507101697).send("```" + errorMsg + "```")

  # for guild in client.guilds:
  #   for textChannel in guild.text_channels:
  #     await textChannel.send("Hey Everyone! I am up and raring to go OwO")

@client.event
async def on_message(message):
  try:
    if message.author == client.user:
      return

    if myBot.asleep:
      result = [await f.sleeping_protocol(myBot, message)]
      if not myBot.asleep:
        result.append(await f.coin_flip(message))
        result.append(await f.roll_dice(message))
        result.append(await f.dialogue_handler(client, message))
        result.append(await f.reaction_handler(client, message))
    else:
      result = [await f.sleeping_protocol(myBot, message), await f.coin_flip(message), await f.roll_dice(message), await f.dialogue_handler(client, message), await f.reaction_handler(client, message)]

    if 0 in result:
      raise Exception("Something went wrong: " + str(result))

  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")

@client.event
async def on_error(event, args, kwargs):
  for guild in client.guilds:
    await guild.get_channel(625049807140159529).send("Oopsies, Sorry Everyone! I'm causing problems :slight_frown:! I'll sleep it off!\n Error Event: " + str(event) + "\n Args: " + str(args) + "\n Kwargs: " + str(kwargs))
    await myBot.oyasumi()
  return

@client.event
async def on_typing(channel, user, when):
  async with channel.typing():
      await asyncio.sleep(3)
  await channel.send("Dones!")
  return

@client.event
async def on_message_delete(message):
  for guild in client.guilds:
    await guild.get_channel(801533100588269609).send("==================\nMessage Type: Deletion\nAuthor: " + str(f.extract_names(message.author)[0]) + "\nContent: " + str(message.content) + "\n==================")
  return

@client.event
async def on_message_edit(before, after):
  for guild in client.guilds:
    await guild.get_channel(801533100588269609).send("==================\nMessage Type: Edit\nAuthor: " + str(f.extract_names(before.author)[0]) + "\nContent (Before): " + str(before.content) + "\nContent (After): " + str(after.content) + "\n==================")
  return

@client.event
async def on_reaction_add(reaction, user):
  await reaction.message.add_reaction(reaction.emoji)
  return

@client.event
async def on_disconnect():
  try:
    for guild in client.guilds:
      await guild.get_channel(625049807140159529).send("Sorry Everyone! I'll be back in a bit, having some... technical... difficulties.")
  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    for guild in client.guilds:
        await guild.get_channel(800872499507101697).send("```" + errorMsg + "```")
  return

@client.event
async def on_reaction_remove(reaction, user):
  await reaction.message.remove_reaction(reaction.emoji)
  return

@client.event
async def on_member_join(member):
  for guild in client.guilds:
    await guild.get_channel(801521814692954153).send("Let Welcome Our New Member Everyone! Everyone say hello to " + str(member.name) + " :partying_face:")
  return

@client.event
async def on_member_remove(member):
  await guild.get_channel(801521814692954153).send("Sorry Everyone, *sniff*, I'm afraid that " + str(member.name) + " has left the server :sob:!")
  return

@client.event
async def on_guild_emojis_update(guild, before, after):
  return

@client.event
async def on_guild_role_update(before, after):
  return


client.run(os.getenv('TOKEN'))



