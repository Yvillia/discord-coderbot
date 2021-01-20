import sys
import numpy as np

def check_multiples(msg):
  '''
  Check how many dice are being asked to be thrown

  Parameters:
  msg - discord.client.message object storing the received message
  
  returns number of dice thrown
  '''
  msg = msg.strip()
  msg = msg[::-1]
  i = 0
  while i < len(msg) and msg[i].isdigit():
    i += 1
  if i == 0: return -1
  else:
    number_of_dice = int(msg[0:i][::-1])
    return number_of_dice

def extract_names(name):
  '''
  Function to separate discord username from id

  Parameters:
  name - discord.client.author object
  
  returns Username and UserID

  '''
  if (type(name) != "string"):
    name = str(name)
  name = name.split("#", 1)
  user = name[0]
  id = name[1]
  return user, id

async def coin_flip(message):
  '''
  Has the bot flip a coin and send the results.
  Responds to Flip and Coin in the same sentence

  Parameters:
  message - discord.client.message object storing the received message

  returns 1 on proper execution
  '''
  try:
    if 'coin' in message.content.lower().strip() and 'flip' in message.content.lower().strip():
        if np.random.randint(0, high=2) == 0:
          await message.channel.send("Heads")
        else:
          await message.channel.send("Tails")
  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")
    return 0
  return 1

async def roll_dice(message):
  '''
  Rolls a die based on the message input

  Parameters:
  message - discord.client.message object storing the received message

  return 1 on proper execution
  '''
  try:
    if 'roll' in message.content.lower().strip() and 'd' in message.content.lower():
        msg = message.content.lower().split('d', 1)
        start = msg[1]
        die_count = check_multiples(msg[0])
        if die_count == -1: die_count = 1
        faces = ''
        for i in start:
          if (i.isdigit()):
            faces += i
        if faces == '':
          await message.channel.send("Try Something Else Plz Dummy!")
          return

        faces = int(faces)
        if faces <= 0 or die_count > 100:
          await message.channel.send("Try Something Else Plz Dummy!")
          return
        else:
          results = [np.random.randint(1, high=(faces+1)) for _ in range(die_count)]
          if len(results) > 1:
            output = "Total Roll: " + str(die_count) + "d" + str(sum(results))
            for i, result in enumerate(results):
              output += "\nRoll " + str(i + 1) + ": 1d" + str(result)
              if result == 1 or result == faces:
                await message.add_reaction("<:thinkban:776586606358167602>")

          else:
            output = str(die_count) + "d" + str(results[0])
          if die_count == sum(results) or die_count * faces == sum(results):
            await message.add_reaction("<:thinkban:776586606358167602>")
          await message.channel.send(output)
  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")
    return 0
  return 1  

async def dialogue_handler(client, message):
  '''
  Handles dialogue responses for bot

  Parameters:
    client - discord.client object (the bot user itself)
    message - discord.client.message object being responded to

  returns 1 on proper execution
  '''
  try:
    if len(message.mentions) > 0:
      for name in message.mentions:
        if "coderbot" == extract_names(name).lower():
          msg = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamp. {0}, Come here\")```"
          await message.channel.send(msg.format(extract_names(message.author)[0]))

      if 'pogchamp' in message.content.lower():
        if len(message.mentions) == 1:
          output = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamp. {0}, Come here\")```".format(extract_names(message.mentions[0])[0])
        else:
          editedStr = ''
          for i, user in enumerate(message.mentions):
            if i != (len(message.mentions) - 1):
              editedStr += str(extract_names(user)[0]) + ", "
            else:
              editedStr += "and " + str(extract_names(user)[0])
          output = "```System.out.println(\"Sigh... Okay, I guess you can be my little Pogchamps. {0}, Come here\")```".format(editedStr)
        await message.channel.send(output)
  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")
    return 0
  return 1

async def reaction_handler(client, message):
  '''
  Similar to dialogue_handler, adds reaction emotes to certain messages

  Parameters:
    client - discord.client object (the bot itself)
    message - discord.client.message object being responded to

  returns 1 for correct 
  '''
  try:
    if "shit" in message.content.lower():
      await message.add_reaction(":poop:")

    if str(message.author) == "Mat#5553" and np.random.randint(1, 21) == 1:
      await message.add_reaction("<:thinkban:776586606358167602>")

    if str(message.author) == "PokeProfRob#2670" and np.random.randint(1, 21) == 1:
      await message.add_reaction("<:mat:792252631765483520>")

    if message.content.lower().startswith('poll:'):
        await message.add_reaction("✅")
        await message.add_reaction("❌")

  except Exception as inst:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
    await message.channel.send("```" + errorMsg + "```")
    return 0
  return 1

  
  
