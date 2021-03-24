import asyncio
import time
from datetime import datetime, timedelta

import discord


class Bot:
    def __init__(self, client_in, ids):
        self.status = "Status: Zzzzzz... "
        self.client = client_in
        self.asleep = True
        self.IDs = ids
        self.tweets = []

    async def oyasumi(self):
        sleeping = discord.Game("State: Asleep")
        await self.client.change_presence(activity=sleeping)
        self.asleep = True

    async def awaken(self):
        awake = discord.Game("State: Awake")
        await self.client.change_presence(activity=awake)
        self.asleep = False

    def reportStatus(self):
        if self.asleep:
            self.status = "Status: Zzzzzz... "
        else:
            self.status = "Status: I'm Awake and Healthy Everyone!"
        time.sleep(600)

        return

    def updateInformation(self, channels, guildID, myID):
        self.channels = channels
        self.guildID = guildID
        self.myID = myID
