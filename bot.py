import discord
from datetime import datetime, timedelta
import asyncio
import time

class Bot:  
  def __init__(self, client_in, ids):
    self.status = ""
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

  def reportStatus(self):
    if self.asleep:
      self.status = "Status: Zzzzzz... "
    else:
      self.status = "Status: I'm Awake and Healthy Everyone!"

    if datetime.now().minute != 0:
      minute = 0
      now = datetime.now()
      future = datetime(now.year, now.month, now.day, now.hour, minute)
      if now.minute > minute:
          future += timedelta(hours=1)
      time.sleep((future-now).seconds)
    else:
      time.sleep(600)
    
    return

  def updateInformation(self, channels, guildID, myID):
    self.channels = channels
    self.guildID = guildID
    self.myID = myID
