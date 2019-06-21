import discord
import os
import psycopg2
import pixivpy3
from pybooru import Danbooru
import praw
from commands import commands

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
        output = commands.custom(message, conn)
        await message.channel.send(output)

    elif message.content.startswith("yi!"):
        output = commands.call_custom(message, conn)
        await message.channel.send(output)

    elif message.content.startswith("remove:"):
        output = commands.remove(message, conn)
        await message.channel.send(output)

    elif message.content == "list!":
        output = commands.cclist(conn)
        await message.channel.send(output)

    elif message.content.startswith("pixiv!"):
        await commands.pixiv(message, api, os, discord)

    elif message.content.startswith("danbooru!"):
        output = commands.danbooru(message, danb, oldposts)
        await message.channel.send(output)

    elif message.content.startswith("reddit!"):
        output = commands.reddit_get(message, reddit, oldsubmissions)
        await  message.channel.send(output)

    elif message.content == "yikes!":
        await commands.yikes(message, discord)

client.run(token)
