import discord
import os
import sys
from bot import Bot 
import function as f

client = discord.Client()
awake = discord.Game("State: Awake")
myBot = Bot(client)

@client.event
async def on_ready():
  try: 
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity = awake)
  
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
    else:
      result = [await f.sleeping_protocol(myBot, message), await f.coin_flip(message), await f.roll_dice(message), await f.dialogue_handler(client, message), await f.reaction_handler(client, message)]

    if 0 in result:
      raise Exception("Something went wrong: " + str(result))

  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")

client.run(os.getenv('TOKEN'))



