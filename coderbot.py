import discord
import os
import numpy as np

client = discord.Client()

def check_multiples(msg):
  i = -1
  while msg[i].isdigit() and abs(i) < len(msg):
    i -= 1
  if i == -1: return 0
  else:
    number_of_dice = int(msg[i:-1])
    return number_of_dice

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  try:
    if message.author == client.user:
      return
  
    if str(message.author) == "Mat#5553":
      await message.add_reaction("<:thinkban:776586606358167602>")

    if 'coin' in message.content.lower().strip() and 'flip' in message.content.lower().strip():
      if np.random.randint(0, high=2) == 0:
        await message.channel.send("Heads")
      else:
        await message.channel.send("Tails")
    
    if 'roll' in message.content.lower().strip() and 'd' in message.content.lower():
      msg = message.content.lower().split('d', 1)
      start = msg[1]
      die_count = check_multiples(msg[0])
      faces = ''
      for i in start:
        if (i.isdigit()):
          faces += i
      faces = int(faces)
      if faces <= 0:
        await message.channel.send("Try Something Else Dummy")
      else:
        results = [np.random.randint(1, high=(faces+1)) for _ in die_count]
        if len(results) > 1:
          output = "Total Roll: " + str(die_count) + "d" + str(sum(results))
          for i, result in enumerate(results):
            output += "\nRoll " + str(i) + ": 1d" + str(result)
        else:
          output = str(die_count) + "d" + str(np.random.randint(1, high=(faces+1)))
        await message.channel.send(output)


    if message.content.lower().startswith('poll:'):
      await message.add_reaction("✅")
      await message.add_reaction("❌")

    if 'code' in message.content.lower():
      msg = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamp {0}, Come here\")```"
      await message.channel.send(msg.format(str(message.author).split('#', 1)[0]))

  except Exception as inst:
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst.args) + " \n" + str(inst)
    await message.channel.send("```" + errorMsg + "```")

client.run(os.getenv('TOKEN'))



