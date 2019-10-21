import discord
import os
import time
import psycopg2
import pixivpy3
from pybooru import Danbooru
import praw
from commands import commands, customcommands, imagegrabber, search, scorepredictor, hungergames, sourcefinder

#from dotenv import load_dotenv
#load_dotenv()

oldposts = []
oldsubmissions = []
modellist = [0]
friendlistlist = [0]
current_game_channel = None

# initializing shit
token = os.environ.get("TOKEN")
DATABASE_URL = os.environ['DATABASE_URL']
puser = os.environ['PIXIV_USERNAME']
ppass = os.environ['PIXIV_PASSWORD']
client_id = os.environ['REDDIT_CLIENT_ID']
client_secret = os.environ['REDDIT_CLIENT_SECRET']

danb = Danbooru('danbooru')
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='yikes:v1 by u/thennal')

# connecting
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
api = pixivpy3.AppPixivAPI()
api.login(puser, ppass)
client = discord.Client()


print("Running!")
@client.event
async def on_message(message):
    global current_game_channel

    if message.author == client.user:
        return

    serv = message.guild

    # commands
    if message.channel == current_game_channel:
        output = hungergames.game(message)
        if isinstance(output, list):
            if output[-1] == 'Finished!':
                current_game_channel = None
            for event in output:
                await message.channel.send(event)
                time.sleep(3)
        else:
            await message.channel.send(output)

    elif message.content.startswith("peachlator:"):
        output = commands.peachlator(message)
        await message.channel.send(output)

    elif message.content.startswith("word_leaderboard"):
        output = await commands.word_leaderboard(message, serv)
        await message.channel.send(output)

    elif message.content.startswith("score:"):
        output = commands.score(message)
        await message.channel.send(output)

    elif message.content.startswith("strokify:"):
        output = commands.strokify(message)
        await message.channel.send(output)

    elif message.content.startswith("custom:"):
        output = customcommands.custom(message, conn)
        await message.channel.send(output)

    elif message.content.startswith("!"):
        output, noise = customcommands.call_custom(message, conn)
        if not noise:
            await message.channel.send(output)

    elif message.content.startswith("remove:"):
        output = customcommands.remove(message, conn)
        await message.channel.send(output)

    elif message.content == "list!":
        output = customcommands.cclist(conn)
        await message.channel.send(output)

    elif message.content.startswith("pixiv!"):
        await imagegrabber.pixiv(message, api, os, discord)

    elif message.content.startswith("danbooru!"):
        output = imagegrabber.danbooru(message, danb, oldposts)
        await message.channel.send(output)

    elif message.content.startswith("reddit!"):
        output = imagegrabber.reddit_get(message, reddit, oldsubmissions)
        await message.channel.send(output)

    elif message.content.startswith("anime!"):
        output = search.anisearch(message)
        await message.channel.send(output)

    elif message.content.startswith("manga!"):
        output = search.mangasearch(message)
        await message.channel.send(output)

    elif message.content.startswith("score predictor:"):
        output, model, friendlist = scorepredictor.model_creator(message)
        modellist[0] = model
        friendlistlist[0] = friendlist
        await message.channel.send(output)

    elif message.content.startswith("predict:"):
        output = scorepredictor.score_predictor(message, modellist[0], friendlistlist[0])
        await message.channel.send(output)

    elif message.content.startswith("source!"):
        output = sourcefinder.source_from_message(message)
        await message.channel.send(output)

    elif message.content == "hunger games start!":
        if current_game_channel is not None:
            thing = "Due to a cascading series of bad decisions, the game only works in one channel at a time, and" \
                    " there's another game being played somewhere in the universe right now, so fuck you I guess?"
            await message.channel.send(thing)
        else:
            current_game_channel = message.channel
            output = hungergames.initialize(message)
            await message.channel.send(output)

    elif message.content == "yikes!":
        await commands.yikes(message, discord)

    elif message.channel.id == 635538705389584425:
        try:
            msg = message.content.split(" ")
            output_channel = client.get_channel(int(msg[0]))
            await output_channel.send(" ".join(msg[1:]))
        except ValueError:
            await message.channel.send("The first word of the message should be the channel ID.")
        except AttributeError:
            await message.channel.send("Can't find a channel with the given ID.")

    else:
        if "source" not in message.content.lower():
            for attachment in message.attachments:
                output = sourcefinder.sauce_finder(attachment.url)
                if output != 0:
                    await message.channel.send(output)

client.run(token)
