import discord
from datetime import datetime, timedelta
import asyncio

class Bot:  
  def __init__(self, client_in, ids):
    self.client = client_in
    self.asleep = True
    self.IDs = ids

  async def oyasumi(self):
    sleeping = discord.Game("State: Asleep")
    await self.client.change_presence(activity = sleeping)
    self.asleep = True

  async def awaken(self):
    awake = discord.Game("State: Awake")
    await self.client.change_presence(activity = awake)
    self.asleep = False

  async def reportStatus(self):
    if self.asleep:
      for guild in self.client.guilds:
        await guild.get_channel(625049807140159529).send("Status: Zzzzzz... ")
    else:
      for guild in self.client.guilds:
        await guild.get_channel(625049807140159529).send("Status: I'm Awake and Healthy Everyone!")

    if datetime.now().minute != 0:
      minute = 00
      now = datetime.now()
      future = datetime(now.year, now.month, now.day, now.hour, minute)
      if now.minute > minute:
          future += timedelta(hours=1)
      await asyncio.sleep((future-now).seconds)
    else:
      await asyncio.sleep(1800)
    return

  def updateInformation(self, channels, guildID, myID):
    self.channels = channels
    self.guildID = guildID
    self.myID = myID
