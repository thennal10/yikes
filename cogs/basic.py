import os
import re
import json
import random
import psycopg2
import discord
import pint
from wordcloud import WordCloud, STOPWORDS
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']
WORDS = json.load(open('data/fuckrai.json'))
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
ureg = pint.UnitRegistry()


class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"The fuck you want? Latency: `{self.bot.latency*1000:.0f}ms`")

    @commands.command(name='strokify')
    async def strokify(self, ctx, *, input: str):
        """TuRnS gIvEn InPuT tO tHiS"""
        iscap = False
        outputmsg = list(input)
        for count, character in enumerate(outputmsg):
            if character.isalpha():
                if iscap:
                    outputmsg[count] = character.capitalize()
                iscap = not iscap

        await ctx.send("".join(outputmsg))

    @commands.command(name='score')
    async def score(self, ctx, *, input: str):
        """Outputs a score based on the string"""
        num = sum([ord(character) for character in input]) % 11
        await ctx.send(f"bout {num}/10")

    @commands.command(name='wordcloud', aliases=['wc'])
    async def wordcloud(self, ctx, member: discord.Member, channel: discord.TextChannel, number_of_messages: int = 1000):
        """Creates a wordcloud based on the mentioned user"""
        wordstr = ""  # Somewhere to store the words

        perm = channel.permissions_for(ctx.guild.me)
        if perm.read_message_history:
            async for msg in channel.history(limit=number_of_messages):
                if msg.author == member:
                    wordstr += "\n" + msg.content

        stopwords = set(STOPWORDS)
        stopwords = stopwords | {"oh", "yeah", "https", "http", "www", "com", "lol", "lmao",
                                 "that", "imgur", "twitter", "youtube", "youtu"}

        # Create the wordcloud object
        cloud = WordCloud(width=1000, height=1000, margin=0,
                          background_color="white", colormap="tab20",
                          stopwords=stopwords).generate(wordstr)

        cloud.to_file('data/wordcloud.png')
        await ctx.send(file=discord.File('data/wordcloud.png'))

    @commands.command(name='madlibs', brief='What it says on the tin')
    async def madlibs(self, ctx, *, phrase: str):
        """Replaces word types encased in square brackets with random words"""
        # A dict to convert word type aliases to the actual word type
        wordalias = {'noun': 'noun',
                     'n': 'noun',
                     'verb': 'verb',
                     'v': 'verb',
                     'adverb': 'adverb',
                     'adv': 'adverb',
                     'adjective': 'adjective',
                     'adj': 'adjective'}

        # Regex to detect anything in between square brackets
        pattern = re.compile('\[(.*?)\]')
        if not pattern.findall(phrase):
            return await ctx.send("No words to swap given. Enclose a valid word type in square brackets, "
                                  "like ``[noun]``.")

        output = ""
        prev = 0
        iterator = pattern.finditer(phrase)

        try:
            for match in iterator:
                # good luck trying to figure this out in three years
                output += phrase[prev:match.span()[0]] + random.choice(WORDS[(wordalias[match.group()[1:-1]])])
                prev = match.span()[1]
            output += phrase[prev:]

            await ctx.send(output)
        except KeyError as e:
            await ctx.send(f"No idea what ``{e.args[0]}`` is. Valid word types are ``noun`` (``n``), ``verb`` (``v``), "
                           f"``adjective`` (``adj``), and ``adverb`` (``adv``).")

    @commands.command(name='echo')
    @commands.is_owner()
    async def echo(self, ctx, channel: discord.TextChannel, *, message: str):
        """Echo message to a certain channel. Premed only"""
        await channel.send(message)

    @commands.command(name='convert', usage='[quantity] [unit] to [unit]')
    async def convert(self, ctx, *, message: str):
        """Converts a physical quantity to another unit"""
        # Basic input parsing
        if len(message.split(' to ')) > 1:
            messagelist = message.split(' to ')
        else:
            raise commands.UserInputError('Add a `to` between the units you want to convert.')

        # Rest of the input parsing is done by pint
        try:
            original = ureg(messagelist[0])
            converted = original.to(messagelist[1])
            await ctx.send(f"**{original}** is **{converted:.3gP}**")
        # ValueError when unit its converted into has a scaling factor too
        # Like '5lbs to 5kg'
        except (pint.UndefinedUnitError, pint.DimensionalityError, ValueError) as e:
            await ctx.send(e)
        # very specific case when 'to' is included but units aren't
        # if no unit is given, ureg() converts the string to an int, and .to raises an AttributeError
        except AttributeError:
            await ctx.send(f"No unit given to be converted from.")


def setup(bot):
    bot.add_cog(Basic(bot))
