# Discord Coderbot

## Table of Contents
 - [Gist](https://github.com/nnrogers515/discord-coderbot#gist)
 - [Purpose](https://github.com/nnrogers515/discord-coderbot#purpose)
 - [Repository Layout](https://github.com/nnrogers515/discord-coderbot#repository-layout)
 - [Functionalities](https://github.com/nnrogers515/discord-coderbot#functionalities)
 - [Contributors](https://github.com/nnrogers515/discord-coderbot#contributors)

## Gist
Discord Bot for those interested in Anime and Programming Memes (and also a bunch of other fun functionalities!)

## Purpose
This bot has a variety of useful tools that you can call for fun, convenience or for acquiring general information (and will have much more functionality coming forward), but the main purpose of the bot is just to learn more about bot design, machine learning, popular APIs, and general programming techniques that will keep the contributors learning! 

## Installation
Currently in the process of being generalized. As of the current time, the best way to access Coderbot would be to:

1. Fork this codebase 
2. Create a discord bot via the [Developer Portal](https://discord.com/developers/applications) (I recommend [here](https://codeburst.io/discord-bot-tutorial-2020-a8a2e37e347c) for a good and thorough walkthrough!)
3. Give the bot any permissions you want (her @mention functionalities may be buggy unless she has some permissions, but otherwise she works fine for general purpose)
4. Take the bot-id TOKEN from your new application and put it as the "TOKEN" environment variable (either in a .env or as a config variable for hosts such as Heroku), then adjust the IDs within src/coderbot.py to match your channel IDs (found sending a message in discord containing "\#Channel-Name"

<em> However, That Sounds Like a Lot of Work! </em>

We are working to streamline this! We will try to make this as least painful as possible moving forward, but for now, if you are interested in using the bot, and stuck on setting it up, let me know via email to yvillia-bot@gmail.com or in the discussions, and I will do my best to help you!

## Repository Layout
- .github/ - Contains Workflow and Issue Templates
- src/     - Contains Python Backend for Coderbot
    - bot.py - Classfile for Coderbot. Contains State Information and Discord Client Instance
    - coderbot.py - General Discord Client Event Responses and Commands
    - function.py - Helper Functions and Handlers for Dialogue, Reactions, and Commands
    - redditAPI.py - Initializes a Reddit Instance using Coderbot's Reddit Credentials
    
- test/    - Contains unit testing for functions
    - test_bot.py - Unit Tests for bot.py Class Functions
    - test_coderbot.py - Unit Tests for coderbot.py Discord Event Handlers
    - test_function.py - Unit Tests for Helper Functions and Handlers
    - test_redditAPI.py - Unit Test of Reddit Instance Initialization
    
- websrc/  - Contains frontend components for Django Heroku Webapp
    - Still in Development

- .replit - If you want to code on Repl.it
- Dockerfile - If you want to try to containerize Coderbot
- Procfile - For Heroku Worker Dyno (also the commands for local execution)

## Functionalities
  Sample Functionalities:
  - !Poll - Produces Emote Reactions on Message for Suitible for Polls
  - !Flip or !Coin - Returns "Heads" or "Tails" on Request
  - !Roll #d# - Return the result of dice rolls where the # before the d represents the number of dice thrown (maximum 100 for performance and spam prevention reasons), and the number after the d represents the number of faces on each die.
  - !Help - Displays a List of Commands
  - !Pogchamp @mention ... - Fun Chat Command
  - !Ban @mention ... - Not a Ban but a Punishment!
  - Sleep and Awake Protocols - If you find her to be annoying, simply tell her to sleep with "Oyasumi" and she won't answer commands until woken up with "Ohayo", you can see her current state under her profile in discord
  - Good Bot and Bad Bot, as well as list functionalities will be coming soon, along with a bunch of other features
  - !Kill - Emergency use kill switch will make her logout of discord and will require a server restart for her to come back (she shouldn't have any spamming
  
  For more documentation checkout the Wiki Pages (when they are finished!)

## Contributors
  If you are interested in contributed to the codebase, just email me at yvillia-bot@gmail.com or contact me in some other way! Alway welcoming new people, Although the generality of Coderbot is still currently in the works, so it will be a little while before it is easy to incorporate her into another's server! 
  
## Future Functionalities/Ideas for Development

<!-- issueTable -->

<!-- issueTable -->


