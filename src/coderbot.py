import asyncio
import json
import os
import sys
import threading
import time
from datetime import datetime, timedelta
import redis

import discord
from discord.ext import commands, tasks

import function as f
from bot import Bot
from redditAPI import redditAPI
from twitter.twitter_utils import twitter_update
intents = discord.Intents.default()
intents.members = True

# List of Discord IDs for Bot Channels
# #Real Channels, uncomment this before merging
# # ID = {
# #   'serverID': 625041679325462571,
# #   'statusID': 625049807140159529,
# #   'commentaryID': 801521814692954153,
# #   'bottestID': 800872499507101697,
# #   'archiveID': 801533100588269609,
# #   'musicID': 801529894899154996,
# #   'coderbotID': 800867858913165333,
# #   'awwID': 802393034104242199,
# #   'uiucID': 802393049459195914,
# #   'dataisbeautifulID': 802393080417615882,
# #   'learnprogrammingID': 802393170356600854,
# #   'programmerhumorID': 802393191046840345,
# #   'ffxivID': 802393280721584138
# # }

# #Test Channels, comment this before merging
# ID = {
#   'serverID': 614887444591935498,
#   'statusID': 614892196738498569,
#   'commentaryID': 614887444591935584,
#   'coderbotID': 337998244317495317
# }

with open("channelConfig.json") as channelConfigFile:
    ID = json.load(channelConfigFile)

REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
REDDIT_USER = os.getenv("REDDIT_USER")
REDDIT_PASS = os.getenv("REDDIT_PASS")

# Client Spinup
client = discord.Client(intents=intents)

# Made this resilient if reddit API stuff isn't found
redd_inst = None
# Reddit API Instance
if REDDIT_ID is not None:
    redd_inst = redditAPI(REDDIT_ID, REDDIT_SECRET, REDDIT_USER, REDDIT_PASS)
else:
    print("QwQ I'm sowwy... I can't see the weddit api...")

subreddit_list = []
if redd_inst is not None:
    subreddit_list = [
        # redd_inst.reddit.subreddit("aww"),
        # redd_inst.reddit.subreddit("learnprogramming"), redd_inst.reddit.subreddit("programmerhumor"),
        redd_inst.reddit.subreddit("dataisbeautiful"),
        # redd_inst.reddit.subreddit("UIUC"),
        # redd_inst.reddit.subreddit("ffxiv")
    ]

# Asleep Status for Bot Avatar
asleep = discord.Game("State: Asleep")

# Bot Class Intialization
myBot = Bot(client, ID)

# redis
r = redis.Redis(host='localhost', port=6379, db=0)

# task_manager = commands.Bot(command_prefix="!", intents=intents)


@tasks.loop(hours=24.0)
async def post_saved():
    # print("here")
    # for saved_post in redd_inst.me.saved(limit=None):
    #   print(saved_post)
    # redd_inst.reddit.submission(id=saved_post.id).unsave()
    for subreddit in subreddit_list:
        curr_channel = myBot.channels[str(subreddit.display_name).lower()]
        await curr_channel.send(datetime.now())
        for hot_post in subreddit.hot(limit=1):
            await curr_channel.send(hot_post.url)


@tasks.loop(hours=0.5)
async def send_message():
    now = datetime.now()
    if now.minute != 0 or now.minute != 30:
        if now.minute < 15 or now.minute > 45:
            minute = 0
        else:
            minute = 30

        future = datetime(now.year, now.month, now.day, now.hour, minute)
        if now.minute > minute:
            future += timedelta(hours=1)
        await asyncio.sleep((future - now).seconds)

    await asyncio.sleep(3)
    if myBot.status != "":
        await myBot.channels["status"].send(myBot.status)

@tasks.loop(seconds=15.0)
async def check_tweets():
    print('checking tweets')
    keys = r.keys('*link*')
    print(keys)
    for key in keys:
        link = r.get(key.decode())
        await myBot.channels['stock-updates'].send(link.decode())
        r.delete(key.decode())

@client.event
async def on_ready():
    try:
        # Epic Coders Guild Object
        epicGuild = client.get_guild(ID["serverID"])

        # CoderBot Member Object
        coderBot = epicGuild.get_member(ID["coderbotID"])

        # Dictionary of Channel Objects
        channels = {}
        for name, id in zip(ID.keys(), ID.values()):
            if name == "serverID":
                continue
            channels.update({name[:-2]: epicGuild.get_channel(id)})

        # Creating Status Reporting Thread
        threading.Thread(target=f.schedule_thread, args=(myBot,)).start()

        # Update Asynchronous Information After Client Login
        myBot.updateInformation(channels, epicGuild, coderBot)

        # Start up twitter bot
        print('starting')
        threading.Thread(target=twitter_update, args=()).start()
        print('ending')

        # Success and Bot Starts Up in Sleep State
        print("\n Logged in as: {0.user}\n".format(client))
        await client.change_presence(activity=asleep)

        # Availability Indicator and Half-Hourly Status Report
        await myBot.channels["status"].send(
            "Hey Everyone! I am alive and sleepy! Wake me up if ya need me OwO!"
        )

        # Reddit Tasks Begin
        post_saved.start()

        # Status Update Task Begin
        send_message.start()

        # start reading tweets
        check_tweets.start()

    except Exception as inst:
        _, _, exc_tb = sys.exc_info()
        errorMsg = (
            "Error "
            + str(type(inst))
            + ": \n"
            + str(inst)
            + "\nLine: "
            + str(exc_tb.tb_lineno)
        )
        await myBot.channels["bottest"].send("```" + errorMsg + "```")


@client.event
async def on_message(message):
    try:
        # If Bot Sends the Message Return !!! DO NOT REMOVE !!!
        if message.author == client.user:
            return

        # Kill Switch
        #     if "!kill" in message.content.lower() and str(message.author) != "Mat#5553":
        #       await myBot.channels['status'].send("Process Killed: Sorry Guys :sob:!")
        #       await client.logout()

        pack = (myBot, message)
        # Allow Only Sleeping Protocols While Bot is Asleep
        if myBot.asleep:
            result = [await f.sleeping_protocol(*pack)]
            if not myBot.asleep:
                # Process with Other Functions if Bot Wakes up
                result.extend(
                    [
                        await f.coin_flip(*pack),
                        await f.roll_dice(*pack),
                        await f.dialogue_handler(*pack),
                        await f.reaction_handler(*pack),
                    ]
                )
        else:
            # Process all Functions as Long as Bot is Awake
            result = [
                await f.sleeping_protocol(*pack),
                await f.coin_flip(*pack),
                await f.roll_dice(*pack),
                await f.dialogue_handler(*pack),
                await f.reaction_handler(*pack),
            ]

        # Indicates which Functions May Have Had Errors
        if 0 in result:
            raise Exception("Something went wrong: " + str(result))

    except Exception as inst:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errorMsg = (
            "Error "
            + str(type(inst))
            + ": \n"
            + str(inst)
            + "\nLine: "
            + str(exc_tb.tb_lineno)
        )
        await message.channel.send("```" + errorMsg + "```")


@client.event
async def on_error(event, *args, **kwargs):
    # Error Message and Sets Bot to Asleep
    await myBot.channels["archive"].send(
        "Oopsies, Sorry Everyone! I'm causing problems :slight_frown:! I'll sleep it off!\n Error Event: "
        + str(event)
        + "\n Args: "
        + str(args)
        + "\n Kwargs: "
        + str(kwargs)
    )
    await myBot.oyasumi()
    return


# @client.event
# async def on_typing(channel, user, when):

#   return


@client.event
async def on_message_delete(message):
    # Store Messages in Archive So Everyone Can Have Message Privileges
    if str(message.author).lower() == "coderbot":
        return

    # Store Deleted Messages in Archive So Everyone Can Have Message Privileges
    await myBot.channels["archive"].send(
        "==================\nMessage Type: Deletion\nAuthor: "
        + str(f.extract_names(message.author)[0])
        + "\nContent: "
        + str(message.content)
        + "\n=================="
    )
    return


@client.event
async def on_message_edit(before, after):
    if str(before.author).lower() == "coderbot":
        return

    # Store Messages in Archive So Everyone Can Have Message Privileges
    await myBot.channels["archive"].send(
        "==================\nMessage Type: Edit\nAuthor: "
        + str(f.extract_names(before.author)[0])
        + "\nContent (Before): "
        + str(before.content)
        + "\nContent (After): "
        + str(after.content)
        + "\n=================="
    )
    return


@client.event
async def on_reaction_add(reaction, user):
    if not myBot.asleep:
        await reaction.message.add_reaction(reaction.emoji)
    return


# @client.event
# async def on_disconnect():
#   try:
#     await myBot.channels['status'].send("Sorry Everyone! I'll be back in a bit, having some... technical... difficulties.")

#   except Exception as inst:
#     _, _, exc_tb = sys.exc_info()
#     errorMsg = "Error " + str(type(inst)) + ": \n" + str(inst) + "\nLine: " + str(exc_tb.tb_lineno)
#     await myBot.channels['bottest'].send("```" + errorMsg + "```")
#   return


@client.event
async def on_raw_reaction_remove(payload):
    # print(payload.channel_id, payload.guild_id, payload.member, payload.message_id)
    # reaction = payload.emoji
    # member_self = await client.get_guild(625041679325462571).get_member(800867858913165333)
    # await reaction.message.channel.send("Triggered")
    # print(member_self)
    # await reaction.message.remove_reaction(reaction.emoji, myBot.myID)
    return


@client.event
async def on_member_join(member):
    await myBot.channels["commentary"].send(
        "Let Welcome Our New Member Everyone! Everyone say hello to "
        + str(member.name)
        + " :partying_face:"
    )
    return


@client.event
async def on_member_remove(member):
    await myBot.channels["commentary"].send(
        "Sorry Everyone, *sniff*, I'm afraid that "
        + str(member.name)
        + " has left the server :sob:!"
    )
    return


@client.event
async def on_guild_emojis_update(guild, before, after):
    return


@client.event
async def on_guild_role_update(before, after):
    return


if not os.getenv("TOKEN") is None:
    client.run(os.getenv("TOKEN"))
else:
    print("TOKEN environment variable not found")
