import asyncio
import json
import sys
import threading

import discord
import numpy as np
import requests
import sympy
from discord import File
from PIL import Image
from sympy import S, latex, preview
from sympy.core.numbers import Float as symFloat
from sympy.core.numbers import Integer as symInt
from sympy.parsing.latex import parse_latex
from sympy.plotting.plot import Plot as symPlot

# async def reminder(timer_len):


def schedule_thread(myBot):
    while True:
        myBot.reportStatus()
    return


def check_multiples(msg):
    """
    Check how many dice are being asked to be thrown

    Parameters:
    msg - discord.client.message object storing the received message

    returns number of dice thrown
    """
    # Reverses String Before d
    msg = msg.strip()
    msg = msg[::-1]
    i = 0
    while i < len(msg) and msg[i].isdigit():
        i += 1
    if i == 0:
        return -1  # If No Given Numbers Return -1
    else:
        # Reverses Again After Finding When the Numbers Stop
        number_of_dice = int(msg[0:i][::-1])
        return number_of_dice


def extract_names(name):
    """
    Function to separate discord username from id

    Parameters:
    name - discord.client.author object

    returns Username and UserID

    """
    if type(name) != "string":
        username = str(name)
    username = username.split("#", 1)
    user = username[0]
    id = username[1]
    return user, id


async def coin_flip(myBot, message):
    """
    Has the bot flip a coin and send the results.
    Responds to Flip and Coin in the same sentence

    Parameters:
    myBot - Coderbot Class Found in bot.py
    message - discord.client.message object storing the received message

    returns 1 on proper execution
    """
    try:
        if (
            "!coin" in message.content.lower().strip()
            or "!flip" in message.content.lower().strip()
        ):
            if np.random.randint(0, high=2) == 0:
                await message.channel.send("Heads")
            else:
                await message.channel.send("Tails")
    except Exception as inst:
        return await fuckup(inst, message)
    return 1


async def roll_dice(myBot, message):
    """
    Rolls a die based on the message input

    Parameters:
    myBot - Coderbot Class Found in bot.py
    message - discord.client.message object storing the received message

    return 1 on proper execution
    """
    try:
        stripped_msg = message.content.lower().strip()
        if (
            "roll:" in stripped_msg
            or "!roll" in stripped_msg
            or "!dice" in stripped_msg
            or "!die" in stripped_msg
        ) and "d" in stripped_msg:
            msg = message.content.lower().split("d", 1)
            start = msg[1]
            die_count = check_multiples(msg[0])
            if die_count == -1:
                die_count = 1
            faces = ""
            for i in start:
                if i.isdigit():
                    faces += i
            if faces == "":
                await message.channel.send("Try Something Else Plz Dummy!")
                return

            faces = int(faces)
            if faces <= 0 or die_count > 100:
                await message.channel.send("Try Something Else Plz Dummy!")
                return
            else:
                results = [
                    np.random.randint(1, high=(faces + 1)) for _ in range(die_count)
                ]
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
        return await fuckup(inst, message)
    return 1


async def ban(message):
    if (
        len(message.mentions) == 1
        and "coderbot" == extract_names(message.mentions[0])[0].lower()
    ):
        if not message.author.top_role.name.lower() == "snail queen":
            await message.channel.send(
                "... Uhh, No thank you? Enjoy your new Username for a Little While Ya Lemon 🤬!"
            )
            og_name = str(message.author.display_name)
            if og_name is None:
                og_name = message.author.name
            if len(og_name) < 24:
                await message.author.edit(nick="Ye Ol' Tart " + og_name)
            else:
                await message.author.edit(nick="Ye Ol' Lemon")
            await asyncio.sleep(10)
            await message.channel.send(
                "Okay... Maybe that a was a bit far. I'm Sowwy 😔"
            )
            await message.author.edit(nick=og_name)
        else:
            await message.channel.send("Uuurgh, you are too powerful to be stopped!")
        return

    elif len(message.mentions) == 1:
        member = message.mentions[0]
        if member.top_role.name.lower() == "snail queen":
            await message.channel.send("Urg!!! They are too powerful to ban!")
        og_name = member.nick  # extract_names(member)[0]
        if og_name is None:
            og_name = member.name
        if type(message.guild.get_member(member.id)) is not None:
            await message.channel.send(
                "OOPSIE WOOPSIE!! Uwu Did Someone make a fucky wucky!?! A wittle fucko boingo!? Better be more Cawreful! Enjoy the Nickname for a little while Ye Ol' Tart {0} ;3!".format(
                    extract_names(member)[0]
                )
            )
            if message.guild.get_member(member.id) is not None:
                if len(og_name) < 24:
                    await message.guild.get_member(member.id).edit(
                        nick="Ye Ol' Tart " + og_name
                    )
                else:
                    await message.guild.get_member(member.id).edit(nick="Ye Ol' Lemon")
                await asyncio.sleep(60)
                await message.channel.send("Okay Ban-Time is Uppers :3")
                await message.guild.get_member(member.id).edit(nick=og_name)

        else:
            await message.channel.send(
                "Umm, Sorry technical difficulties! Are you shore that person exists :3?"
            )
        return

    else:
        editedStr = ""
        for i, user in enumerate(message.mentions):
            if extract_names(user)[0].lower() == "coderbot":
                continue

            if i != (len(message.mentions) - 1):
                editedStr += str(extract_names(user)[0]) + ", "
            else:
                editedStr += "or " + str(extract_names(user)[0])

        await message.channel.send(
            "```Sigh... Okay, guess it's time to drop the ban-hammer. Whose wants this big ol' hammer first :3? {0}, UwU <3<3<3<3 ;3;3;3;3 ????```".format(
                editedStr
            )
        )

        for member in message.mentions:
            if extract_names(member)[0].lower() == "coderbot":
                continue

            if (
                message.guild.get_member(member.id) is not None
                and not message.guild.get_member(member.id).top_role.name.lower()
                == "snail queen"
            ):
                og_name = message.guild.get_member(member.id).nick
                await message.guild.get_member(member.id).edit(
                    nick="Ye Ol' Tart " + og_name
                )
                await asyncio.sleep(60)
                await message.channel.send("Okay, Ban Time Uppers :3")
                await message.guild.get_member(member.id).edit(nick=og_name)


async def pogchamp(message):
    if (
        len(message.mentions) == 1
        and "coderbot" == extract_names(message.mentions[0])[0].lower()
    ):
        output = (
            "... Umm, sure I guess I can be my own little Pogchamp, you bully! :sob:"
        )

    elif len(message.mentions) == 1:
        output = '```System.out.println("Sigh... Okay, I guess you can be my little Pogchamp. {0}, Come here")```'.format(
            extract_names(message.mentions[0])[0]
        )

    else:
        editedStr = ""
        for i, user in enumerate(message.mentions):
            if extract_names(user)[0].lower() == "coderbot":
                continue

            if i != (len(message.mentions) - 1):
                editedStr += str(extract_names(user)[0]) + ", "
            else:
                editedStr += "and " + str(extract_names(user)[0])
        output = '```System.out.println("Sigh... Okay, I guess you can be my little Pogchamps. {0}, Come here")```'.format(
            editedStr
        )

    # Output String is Built in the Conditionals Above and Sent
    await message.channel.send(output)


async def evalMath(message, expression, isLatex=False):
    try:
        # take out backticks
        if "`" in expression:
            expression = expression.replace("`", "")

        if isLatex:
            r = S(parse_latex(expression))
        else:
            r = S(expression)

        preview(r, viewer="file", filename="../imgs/output.png")

        # resize image
        baseheight = 80
        img = Image.open("../imgs/output.png")
        hpercent = baseheight / float(img.size[1])
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), Image.ANTIALIAS)
        img.save("../imgs/output.png")

        # send Image
        lx = latex(r)

        if isLatex:
            msg = "Expression: `{}`".format(parse_latex(expression))
        else:
            msg = "Latex: `{}`".format(lx)

        if isinstance(r, symInt) or isinstance(r, symFloat):
            approx = r.evalf()
            msg = "{}\n`ans = {:.10f}`".format(msg, approx)
            await message.channel.send(msg, file=File("../imgs/output.png"))
        elif isinstance(r, symPlot):
            r.save("../imgs/fig")
            await message.channel.send(
                msg, files=[File("../imgs/fig.png"), File("../imgs/output.png")]
            )
        elif isinstance(r, tuple) or isinstance(r, list):
            new_nums = []
            for i in r:
                if isinstance(r, symInt):
                    new_nums.append(r.evalf())
            if len(new_nums) == len(r):
                list_msg = "["
                for i in new_nums:
                    list_msg = "{},{:.10f}".format(list_msg, i)
                list_msg = list_msg[:-1] + "]"
                msg = "{}\n`ans = {}`".format(msg, list_msg)
            await message.channel.send(msg, file=File("../imgs/output.png"))
        else:
            await message.channel.send(msg, file=File("../imgs/output.png"))

    except Exception as inst:
        return await fuckup(inst, message)


async def dialogue_handler(myBot, message):
    """
    Handles dialogue responses for bot

    Parameters:
      myBot - Coderbot Class Found in bot.py
      message - discord.client.message object being responded to

    returns 1 on proper execution
    """
    try:

        # the bot can't react to its own commands
        # mostly useful with the help command
        if message.author == "CoderBot#9778":
            return

        # Bad Bot and Good Bot Messages With Live Updates to Statistics.json
        if "bad bot" in message.content.lower():
            await good_bot(False, message)
            return

        elif "good bot" in message.content.lower():
            await good_bot(True, message)
            return

        # Magic 8ball.
        if "!8ball" in message.content.lower():
            await eightball(message)
            return

        if "!help" in message.content.lower():
            await displayHelp(message)
            return

        # Ban Commentary
        if "!ban" in message.content.lower() and len(message.mentions) == 0:
            await message.channel.send(
                "Umumu, I see you have chosen... Banishment "
                + extract_names(message.author)[0]
                + "!! Bai Bai!"
            )
            await asyncio.sleep(5)
            await message.channel.send("... Juuuuuuusssst Kidding 😜!!!")
            return

        if message.content.startswith("!wiki "):
            wikiName = message.content[6:]
            await getWikiSummary(message, wikiName)
            return

        if message.content.startswith("!math "):
            expression = message.content[6:]
            await evalMath(message, expression)
            return

        if message.content.startswith("!matex "):
            expression = message.content[6:]
            await evalMath(message, expression, isLatex=True)
            return

        # if "!reminder" in message.content.lower():
        #   threading.Thread(target=f.schedule_thread, args=(myBot,)).start()

        # Checks Mentions for Individual/Group Messages
        if len(message.mentions) > 0:
            for name in message.mentions:
                if (
                    "!pogchamp" not in message.content.lower()
                    and "!ban" not in message.content.lower()
                    and extract_names(message.author)[0].lower()
                    == extract_names(name)[0].lower()
                ):
                    msg = '```System.out.println("Sigh... Okay, I guess you can be my little Pogchamp. {0}, Come here")```'
                    await message.channel.send(
                        msg.format(extract_names(message.author)[0])
                    )
                    return

            if (
                "!ban" in message.content.lower()
                and "pogchamp" in message.content.lower()
            ):
                await message.channel.send(
                    "STOP, I'LL NEVER BAN MY LITTLE POGCHAMPS!!! YOU CAN'T MAKE ME 😖!"
                )
                return

            elif "!ban" in message.content.lower():
                await ban(message)
                return
            elif "!pogchamp" in message.content.lower():
                await pogchamp(message)
                return
    except Exception as inst:
        return await fuckup(inst, message)

    return 1


async def reaction_handler(myBot, message):
    """
    Similar to dialogue_handler, adds reaction emotes to certain messages

    Parameters:
      myBot - Coderbot Class Found in bot.py
      message - discord.client.message object being responded to

    returns 1 for correct
    """

    try:
        if str(message.author) == "Mat#5553" and np.random.randint(1, 21) == 1:
            await message.add_reaction("<:thinkban:776586606358167602>")

        if str(message.author) == "PokeProfRob#2670" and np.random.randint(1, 21) == 1:
            await message.add_reaction("<:mat:792252631765483520>")

        if message.content.lower().startswith(
            "poll:"
        ) or message.content.lower().startswith("!poll"):
            await message.add_reaction("✅")
            await message.add_reaction("❌")

    except Exception as inst:
        return await fuckup(inst, message)
    return 1


async def sleeping_protocol(myBot, message):
    try:
        if myBot.asleep and (
            "ohayo" in message.content.lower()
            or (
                len(message.mentions) > 0
                and extract_names(message.mentions[0])[0].lower()
            )
            == "coderbot"
        ):
            await myBot.awaken()
            await message.channel.send("Good Morning Everyone! :heart:")
            return

        elif not myBot.asleep and (
            "oyasumi" in message.content.lower()
            or "stop bot" in message.content.lower()
            or (
                len(message.mentions) > 0
                and "good night" in message.content.lower().strip()
                and myBot.myID.name in message.mentions
            )
        ):
            # and extract_names(message.author)[0].lower() == "yvillia":
            await message.channel.send(
                "Like totally nighty-nighters everyone! :kissing_heart:"
            )
            await myBot.oyasumi()
            return

        else:
            return

    except Exception as inst:
        return await fuckup(inst, message)
    return 1


async def good_bot(isGood, message):
    """
    Outputs a message depending on whether the user said good bot or bad bot
    then log the data in statistics.json

    Parameters:
      isGood - boolean used to say if the bot is good or not
      message - discord.client.message object being responded to

    returns 1 for correct
    """
    try:
        response = ""
        dataLog = ""
        if isGood:
            response = (
                "Thank youwo vewwy muwuch! I will continuwue towo dowo my best OwO!"
            )
            dataLog = "Good Bot"
        else:
            response = "I am so sowwry! I prowomise towo dowo better UwU!"
            dataLog = "Bad Bot"

        await message.channel.send(response)
        # Statistics JSON File
        with open("statistics.json", "r") as stats:
            data = json.load(stats)
            stats.close()
        with open("statistics.json", "w") as stats:
            data["Phrases"][dataLog] += 1
            json.dump(data, stats)
            stats.close()
        return 1
    except Exception as inst:
        return await fuckup(inst, message)


async def eightball(message):
    """
    Returns a prophecy based on the hard science of magic8ballism

    Parameters:
      message - discord.client.message object being responded to

    returns 1 upon successful execution
    """
    try:
        if len(message.content) <= 7:
            await message.channel.send("U gotta ask a question dummy!")
            return

        randNum = np.random.randint(1, 6)

        prophecy = ""

        if randNum == 1:
            prophecy = "No x3c"
        elif randNum == 2:
            prophecy = "I'm sowwy... I don't think so QwQ"
        elif randNum == 3:
            prophecy = "Ya uwu"
        elif randNum == 4:
            prophecy = "Most likely owo"
        elif randNum == 5:
            prophecy = "I dunno nwn"
        else:
            prophecy = "Mayb, mayb not 83"

        await message.channel.send(prophecy)
        return 1
    except Exception as inst:
        return await fuckup(inst, message)


async def getWikiSummary(message, title):
    """
    Display the wikipedia article summary of the article with the given title

    Parameters:
      message  - discord.client.message object being responded to
      title - string of the wikipedia article title
    """
    try:
        query = (
            "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles="
            + title
        )
        wikiRequest = requests.get(query)
        summaryObject = wikiRequest.json()

        if list(summaryObject["query"]["pages"])[0] == "-1":
            await message.channel.send(
                "I'm sowwy, I couldn't find " + title + " on wikipedia pwq"
            )
            return 0

        # Grab the wiki summary from the JSON object
        # this line took forever to figure out
        summary = list(summaryObject["query"]["pages"].values())[0]["extract"]

        summary = trimTo2K(summary)

        await message.channel.send(summary)

        # Now for the fucking image
        # if it got this far we know the article exists so no need to check for that
        imageQuery = (
            "https://en.wikipedia.org/w/api.php?action=query&titles="
            + title
            + "&prop=pageimages&format=json&pithumbsize=200"
        )
        wikiImageRequest = requests.get(imageQuery)
        imageSummaryObject = wikiImageRequest.json()

        imageURLObject = list(imageSummaryObject["query"]["pages"].values())[0]

        if "thumbnail" in imageURLObject.keys():
            imageURL = imageURLObject["thumbnail"]["source"]
            await message.channel.send(imageURL)

        return 1

    except Exception as inst:
        return await fuckup(inst, message)


async def displayHelp(message):
    """
    Displays a list of user executable commands

    Parameters:
      message  - discord.client.message object being responded to
    """

    helpMessage = """
  Heya! Here's what I can do for you atm uwu

  ohayo - wake me up owo
  oyasumi - tuck me in o//w//o
  !help - display all commands
  !roll (or !dice/!die) #d## - roll dice
  !flip - flip a coin
  !ban @member - Ban somebody >:3
  !pogchamp @member - Designate one as being a pog champ
  !poll - create a poll
  !wiki [article name] - get wikipedia summary of an article
  !8ball [text] Answer controversial questions
  !math [expression] Check out https://gamma.sympy.org/ for a list of commands
  !matex [latex expresion] Do math in the latex format
  """

    await message.channel.send(helpMessage)
    return


async def fuckup(inst, message):
    """
    Outputs an error that was thrown during the execution of an asynchronous function

    Parameters:
      inst - The Exception object thrown

    returns 0
    """
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
    return 0


# The discord message limit is 2000 characters
# This trims a message to the nearest sentence to 2000 characters
def trimTo2K(message):

    if len(message) <= 2000:
        return message

    i = 2000

    while i >= 0:
        i -= 1
        if message[i] == ".":
            break

    return message[: (i + 1)]
