# Discord Coderbot

## Table of Contents
 - [Gist](https://github.com/nnrogers515/discord-coderbot#gist)
 - [Purpose](https://github.com/nnrogers515/discord-coderbot#purpose)
 - [Repository Layout](https://github.com/nnrogers515/discord-coderbot#repository-layout)
 - [Functionalities](https://github.com/nnrogers515/discord-coderbot#functionalities)
 - [Contributors](https://github.com/nnrogers515/discord-coderbot#contributors)
 - [Current Issues Open for Development](https://github.com/nnrogers515/discord-coderbot#current-issues-open-for-development)
 - [Completed Issues](https://github.com/nnrogers515/discord-coderbot#completed-issues)


## Gist
Discord Bot for those interested in Anime and Programming Memes (and also a bunch of other fun functionalities!)

## Purpose
This bot has a variety of useful tools that you can call for fun, convenience or for acquiring general information (and will have much more functionality coming forward), but the main purpose of the bot is just to learn more about bot design, machine learning, popular APIs, and general programming techniques that will keep the contributors learning!

## Installation

<details>
  <summary> <strong>Click to Expand</strong></summary>
Currently in the process of being generalized. As of the current time, the best way to access Coderbot would be to:

1. Fork this codebase
2. Create a discord bot via the [Developer Portal](https://discord.com/developers/applications) (I recommend [here](https://codeburst.io/discord-bot-tutorial-2020-a8a2e37e347c) for a good and thorough walkthrough!)
3. Give the bot any permissions you want (her @mention functionalities may be buggy unless she has some permissions, but otherwise she works fine for general purpose)
4. Take the bot-id TOKEN from your new application and put it as the "TOKEN" environment variable (either in a .env or as a config variable for hosts such as Heroku), then adjust the IDs within src/coderbot.py to match your channel IDs (found sending a message in discord containing "\#Channel-Name"

<em> However, That Sounds Like a Lot of Work! </em>

We are working to streamline this! We will try to make this as least painful as possible moving forward, but for now, if you are interested in using the bot, and stuck on setting it up, let me know via email to yvillia-bot@gmail.com or in the discussions, and I will do my best to help you!
</details>

## Repository Layout

<details>
  <summary> <strong>Click to Expand</strong></summary>

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
</details>

## Functionalities

<details>
  <summary> <strong>Click to Expand</strong></summary>

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
</details>

## Contributors
  If you are interested in contributed to the codebase, just email me at yvillia-bot@gmail.com or contact me in some other way! Alway welcoming new people, Although the generality of Coderbot is still currently in the works, so it will be a little while before it is easy to incorporate her into another's server!

## Current Issues Open for Development

<details>
  <summary> <strong>Click to Expand</strong></summary>

<!-- openIssueTable -->

| Title                                                                                                                           |         Status          |                                                          Assignee                                                          | Body                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| :------------------------------------------------------------------------------------------------------------------------------ | :---------------------: | :------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/17">Implementing Individual Chatbot Functionalities</a>         | :eight_spoked_asterisk: |                                                                                                                            | Basically utilize ML to have the bot learn from each member, and on command say something that is similar to a given member's speech pattern. This would likely take a while to make, and a very long time to test and make sure that it works properly, but this would be an enjoyable functionality in mimicry!<br /><br /><br />...                                                                                                                                                                            |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/15">Generalize Coderbot Code to work for any discord server</a> | :eight_spoked_asterisk: |                                                                                                                            | This will likely be the most difficult issue. The idea would be to make it as easy as possible for someone to take the Coderbot code and run a script to fill out the necessary server information and so forth. This may require having calls to a Rest API using a user's credentials to login to discord and pull the information in the server from there, or some other path that would require more research into. Due to how this bot operates it will be a bit difficult to setup<br /><br /><br />...    |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/14">Update README.md</a>                                        | :eight_spoked_asterisk: | <a href="https://github.com/nnrogers515"><img src="https://avatars.githubusercontent.com/u/38640928?v=4" width="20" /></a> | The README.md needs better instructions for setting up the bot for other servers and other general important information about the repository.<br /><br /><br />...                                                                                                                                                                                                                                                                                                                                               |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/13">Fix up Git Workflow</a>                                     | :eight_spoked_asterisk: | <a href="https://github.com/nnrogers515"><img src="https://avatars.githubusercontent.com/u/38640928?v=4" width="20" /></a> | Currently, the python workflow doesn't work well with how our repository is setup. I recommend looking at the .github-cli.yaml file, adding security scans and so forth through those tests (for branches outside of master, and maybe add a deploy pipeline).<br /><br /><br />...                                                                                                                                                                                                                               |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/12">Fill out the Coderbot Wiki</a>                              | :eight_spoked_asterisk: |                                                                                                                            | Our Github has a Wikipage that can be utilized as documentation for the bot functionalities. I would recommend collaborating with whoever is working on issue #7 as it is likely there would be an overlap in documentation for these portions.<br /><br /><br />...                                                                                                                                                                                                                                              |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/11">Research Alternatives to Heroku</a>                         | :eight_spoked_asterisk: | <a href="https://github.com/nnrogers515"><img src="https://avatars.githubusercontent.com/u/38640928?v=4" width="20" /></a> | While Heroku is great, it is severely limited with just free memberships. This issue involves researching into Alternatives to Heroku, with the main suggestion being AWS.<br /><br /><br />...                                                                                                                                                                                                                                                                                                                   |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/10">Create Bot Artwork</a>                                      | :eight_spoked_asterisk: |                                                                                                                            | Bot Artwork is currently just a meme of InternetExplorer-chan. It would be cool to have her own artwork or animation instead of a meme picture from my phone.<br /><br />This is really only if there is nothing else to do/someone is interested in doing this, it isn't really coding and requires a lot of time and artistic talent.<br />...                                                                                                                                                                  |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/9">Upgrade bot to run on docker</a>                             | :eight_spoked_asterisk: |                                                                                                                            | Utilizing Docker and a registry would make it easier to create multiple instances of the bot, should the desire for multiple servers become greater. Plus, it's just good for learning.<br /><br /><br />...                                                                                                                                                                                                                                                                                                      |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/8">Bot Emotions</a>                                             | :eight_spoked_asterisk: |                                                                                                                            | Currently the bot only has two states, "Asleep" and "Awake." Once chatbot functionalities have been implemented it would be cool to be able to have her switch states to varying emotions (angry, sad, etc...). <br /><br />This task would be to prepare the framework for having multiple states, likely by making changes to the bot.py class.<br />...                                                                                                                                                        |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/7">Create a Frontend Website for the Bot</a>                    | :eight_spoked_asterisk: |   <a href="https://github.com/RynoXLI"><img src="https://avatars.githubusercontent.com/u/40377123?v=4" width="20" /></a>   | Heroku utilizes a Django python front-end for our bot, which currently is only running a regular worker dyno and not a web dyno. We can create a basic website through Heroku to serve API calls and serve as a monitoring/information gathering site for the bot.<br /><br /><br />...                                                                                                                                                                                                                           |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/6">Implement a database for chat statistics</a>                 | :eight_spoked_asterisk: |                                                                                                                            | Setup and connect the bot using Heroku's database to hold statistics and collected chat information past the running instance. If there is a preferable database alternative to Heroku, then feel free to research into it and try to set up the bot on there.<br /><br /><br />...                                                                                                                                                                                                                               |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/5">Figure out Something Cool to do for the Reddit API</a>       | :eight_spoked_asterisk: |                                                                                                                            | The code base for the RedditAPI is already incorporated and functional. Think of something fun to add that the bot can do by pulling from reddit (i.e. daily image posts, statistics, automatically pulling saved posts and posting them, etc...). RedditAPI documentation found [here](https://praw.readthedocs.io/en/latest/code_overview/reddit_instance.html#praw.Reddit).<br /><br />Note: We are utilizing the PRAW library to make API access easier https://asyncpraw.readthedocs.io/en/latest/.<br />... |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/4">Implement Music Functionality</a>                            | :eight_spoked_asterisk: |                                                                                                                            | This can be anything from playing music on command, to recommending songs that people have been listening to on spotify, or etc... <br /><br /><br />...                                                                                                                                                                                                                                                                                                                                                          |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/3">Reorganize and Document the Code</a>                         | :eight_spoked_asterisk: |                                                                                                                            | Prettify the code a bit and make things more readable. The more organized you can make it the better, just make sure it works. For proper documentation and file organizations see [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html).<br /><br /><br />...                                                                                                                                                                                                                          |
| <a href="https://github.com/nnrogers515/discord-coderbot/issues/1">Enable Chatbot ML Features</a>                               | :eight_spoked_asterisk: |                                                                                                                            | Implement a way to train the bot to respond using machine learning. If possible, live-learning while chatting with others would be beneficial to improving her performance.<br /><br /><br />...                                                                                                                                                                                                                                                                                                                  |

<!-- openIssueTable -->

</details>

## Completed Issues

<details>
 <summary> <strong>Click to Expand</strong></summary>

<!-- closedIssueTable -->

| Title                                                                                                                                       |   Status   | Assignee | Body                                                                                                                                                  |
| :------------------------------------------------------------------------------------------------------------------------------------------ | :--------: | :------: | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a href="https://github.com/nnrogers515/discord-coderbot/pull/22">Format code</a>                                                           | :no_entry: |          | Added pre-commit to repo. The .`pre-commit-config.yaml` contains black, flake8, isortm check-yaml, end-of-file-fixer, and trailing-whitespace hooks.  |
| <a href="https://github.com/nnrogers515/discord-coderbot/pull/21">Format code</a>                                                           | :no_entry: |          | This branch used precommit to format code, to get this to work do the following. <br /><br />`precommit install`<br />...                             |
| <a href="https://github.com/nnrogers515/discord-coderbot/pull/20">Ryan web</a>                                                              | :no_entry: |          | Providing template flask API, and pyTest                                                                                                              |
| <a href="https://github.com/nnrogers515/discord-coderbot/pull/19">Added flask API with examples and example pytest</a>                      | :no_entry: |          | Added flask api, and added pytest for flask.                                                                                                          |
| <a href="https://github.com/nnrogers515/discord-coderbot/pull/18">Kralinc dev</a>                                                           | :no_entry: |          |                                                                                                                                                       |
| <a href="https://github.com/nnrogers515/discord-coderbot/pull/16">Workflow adjust</a>                                                       | :no_entry: |          | updating workflow                                                                                                                                     |
| <a href="https://github.com/nnrogers515/discord-coderbot/pull/2">Fixed code duplication with good_bot() and error messages. Refactored…</a> | :no_entry: |          | … epicID to serverID. Made reddit API resilient against not existing.                                                                                 |

<!-- closedIssueTable -->

</details>
