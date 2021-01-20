import discord
import os
import sys
from function import dialogue_handler, reaction_handler, roll_dice, coin_flip

client = discord.Client()
# guildName = "Epic Coders"
# textChannels = discord.TextChannel(guild=guildName, state=True, data="Nyan")

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  # for guild in client.guilds:
  #   for textChannel in guild.text_channels:
  #     await textChannel.send("Hey Everyone! I am up and raring to go OwO")

@client.event
async def on_message(message):
  try:
    if message.author == client.user:
      return

    result = [await coin_flip(message), await roll_dice(message), await dialogue_handler(client, message), await reaction_handler(client, message)]

    if 0 in result:
      raise Exception("Something went wrong: " + str(result))

  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")

client.run(os.getenv('TOKEN'))



