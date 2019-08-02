import discord
import os
import psycopg2
import pixivpy3
from pybooru import Danbooru
import praw
from commands import commands, customcommands, imagegrabber, search

# from dotenv import load_dotenv
# load_dotenv()


oldposts = []
oldsubmissions = []

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

    if message.author == client.user:
        return

    serv = message.guild

    # commands
    if message.content.startswith("peachlator:"):
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

    elif message.content.startswith("yi!"):
        output = customcommands.call_custom(message, conn)
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

    elif message.content == "yikes!":
        await commands.yikes(message, discord)

client.run(token)
