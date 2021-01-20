import discord

class Bot:  
  def __init__(self, client_in):
    self.client = client_in
    self.asleep = False

  async def oyasumi(self):
    sleeping = discord.Game("State: Asleep")
    await self.client.change_presence(activity = sleeping)
    self.asleep = True

  async def awaken(self):
    awake = discord.Game("State: Awake")
    await self.client.change_presence(activity = awake)
    self.asleep = False


