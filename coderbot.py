import discord
import os
import sys
import numpy as np

client = discord.Client()

def check_multiples(msg):
  msg = msg.strip()
  msg = msg[::-1]
  i = 0
  while i < len(msg) and msg[i].isdigit():
    i += 1
  if i == 0: return 0
  else:
    number_of_dice = int(msg[0:i][::-1])
    return number_of_dice

def extract_names(name):
  if (type(name) != "string"):
    name = str(name)
  name = name.split("#", 1)
  user = name[0]
  id = name[1]
  return user, id


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  try:
    if message.author == client.user:
      return
  
    if str(message.author) == "Mat#5553" and np.random.randint(1, 7) == 6:
      await message.add_reaction("<:thinkban:776586606358167602>")

    if str(message.author) == "PokeProfRob#2670":
      await message.add_reaction("<:mat:792252631765483520>")

    if 'coin' in message.content.lower().strip() and 'flip' in message.content.lower().strip():
      if np.random.randint(0, high=2) == 0:
        await message.channel.send("Heads")
      else:
        await message.channel.send("Tails")
    
    if 'roll' in message.content.lower().strip() and 'd' in message.content.lower():
      msg = message.content.lower().split('d', 1)
      start = msg[1]
      die_count = check_multiples(msg[0])
      if die_count == 0: return
      faces = ''
      for i in start:
        if (i.isdigit()):
          faces += i
      faces = int(faces)
      if faces <= 0:
        await message.channel.send("Try Something Else Dummy")
      else:
        results = [np.random.randint(1, high=(faces+1)) for _ in range(die_count)]
        if len(results) > 1:
          output = "Total Roll: " + str(die_count) + "d" + str(sum(results))
          for i, result in enumerate(results):
            output += "\nRoll " + str(i + 1) + ": 1d" + str(result)
        else:
          output = str(die_count) + "d" + str(np.random.randint(1, high=(faces+1)))
        await message.channel.send(output)

    if message.content.lower().startswith('poll:'):
      await message.add_reaction("✅")
      await message.add_reaction("❌")

    if 'code' in message.content.lower():
        msg = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamp, {0}, Come here\")```"
        await message.channel.send(msg.format(extract_names(message.author)[0]))

    if 'pogchamp' in message.content.lower() and len(message.mentions) > 0:
      if len(message.mentions) == 1:
        output = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamp {0}, Come here\")```".format(extract_names(message.mentions[0])[0])
      else:
        editedStr = ''
        for i, user in enumerate(message.mentions):
          if i != (len(message.mentions) - 1):
            editedStr += str(extract_names(user)[0]) + ", "
          else:
            editedStr += "and " + str(extract_names(user)[0])
        output = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamps, {0}, Come here\")```".format(editedStr)
      await message.channel.send(output)

  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")

client.run(os.getenv('TOKEN'))

