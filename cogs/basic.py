import os
import re
import json
import random
import psycopg2
import discord
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from discord.ext import commands

MIA = 405533644250152960
DATABASE_URL = os.environ['DATABASE_URL']
WORDS = json.load(open('data/fuckrai.json'))
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def leaderboard_name(l):
    name = ""
    for count, element in enumerate(l):
        name += element.capitalize()
        if count != len(l) - 1:
            name += "/"
    return name

async def check_server(ctx):
    if MIA == ctx.guild.id:
        return True
    else:
        await ctx.send("This command is currently disabled for this server.")


class Basic(commands.Cog):
    """BasicCog"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='strokify', help='TuRnS gIvEn InPuT tO tHiS')
    async def strokify(self, ctx, *, input: str):

        iscap = False
        outputmsg = list(input)
        for count, character in enumerate(outputmsg):
            if character.isalpha():
                if iscap:
                    outputmsg[count] = character.capitalize()
                iscap = not iscap

        await ctx.send("".join(outputmsg))

    @commands.command(name='score', help='Outputs a score based on the string')
    async def score(self, ctx, *, input: str):

        num = 0
        for character in input:
            num += ord(character)
        num = (num % 10) + 1

        await ctx.send(f"bout {num}/10")

    @commands.command(name='leaderboard', help='Creates a leaderboard based on a given word/phrase', usage='$leaderboard [no of messages] [phrase1] + [phrase2]...')
    async def word_leaderboard(self, ctx, msglimit: int, *, actmsg: str):

        searchwords = actmsg.split(" + ")
        print(searchwords)
        peeps = [["N/A", 0]]

        for chan in ctx.guild.text_channels:
            perm = chan.permissions_for(ctx.guild.me)
            if perm.read_message_history:
                async for msg in chan.history(limit=msglimit):
                    for searchword in searchwords:
                        if searchword in msg.content.lower() and not msg.author.bot:
                            found = 0
                            for peep in peeps:
                                if msg.author.name == peep[0]:
                                    peep[1] += 1
                                    found = 1
                                    break
                            if found == 0:
                                peeps.append([msg.author.name, 1])
            print(chan)
        peeps.sort(key=lambda x:x[1], reverse=True)

        leaderboard = f"**The {leaderboard_name(searchwords)} Leaderboard**```\nRank  | Name\n\n"
        for count, peep in enumerate(peeps[:10]):
            leaderboard += f"""[{count + 1}]   > {peep[0]}: {peep[1]}\n"""
        leaderboard += "```"
        await ctx.send(leaderboard)

    @commands.command(name='wordcloud', aliases=['wc'], help='Creates a wordcloud based on the mentioned user')
    async def wordcloud(self, ctx, member: discord.Member, channel: discord.TextChannel, lookup_num: int = 1000):
        wordstr = "" # Somewhere to store the words

        perm = channel.permissions_for(ctx.guild.me)
        if perm.read_message_history:
            async for msg in channel.history(limit=lookup_num):
                if msg.author == member:
                    wordstr += " " + msg.content.capitalize()

        # Create the wordcloud object
        cloud = WordCloud(width=1000, height=1000, margin=0,
                          background_color="white", colormap="tab20").generate(wordstr)

        cloud.to_file('data/wordcloud.png')
        await ctx.send(file=discord.File('data/wordcloud.png'))

    @commands.command(name='peachlator', help='What it says on the tin')
    async def peachlator(self, ctx, *, inp: str):
        # get the table
        cur = conn.cursor()
        sql = """SELECT * FROM peachdict;"""
        cur.execute(sql)
        table = cur.fetchall()
        cur.close()

        # made it into a list so I don't have to worry about differing word lengths
        new_message = ["Translation:"] + inp.split()

        # new dict with keys as a list of words
        flattened_dict = {tuple(k[0].split()): k[1] for k in table}


        for key in flattened_dict:
            # indicates the point we're at with the given key
            i = 0
            caps = False
            allcaps = False
            for idx, word in enumerate(new_message):
                if (key[i] == word) or (key[i] == word.lower()):

                    # check if the word is capitalized or in allcaps
                    if key[i].capitalize() == word:
                        caps = True
                    if key[i].upper() == word:
                        allcaps = True

                    i += 1
                    # if we find a valid word
                    if i == len(key):

                        if caps:
                            result = flattened_dict[key].capitalize()
                        elif allcaps:
                            result = flattened_dict[key].upper()
                        else:
                            result = flattened_dict[key]

                        new_message[idx] = result
                        # remove leftover words
                        for r in range(1, i):
                            new_message.pop(idx - r)

                        i = 0

                else:
                    # so that it's a continuous word and not like, splintered across a sentence
                    i = 0
                    caps = False
                    allcaps = False

        await ctx.send(" ".join(new_message))

    @commands.command(name='update_peachlator', help='Update the peachlator', usage='$update_peachlator [word] - [translation]')
    async def update_peachlator(self, ctx, *, inp: str):
        if_MIA = await check_server(ctx)
        if if_MIA:
            data = [word.strip() for word in inp.split("-")]

            if len(data) > 2 or len(data) < 2:
                await ctx.send("Usage: ``$update_peachlator [word] - [translation]``")
                return

            sql = """INSERT INTO peachdict (input, output) VALUES (%s, %s);"""

            cur = conn.cursor()
            try:
                cur.execute(sql, data)
                conn.commit()
                cur.close()
                await ctx.send("Updated!")
            except:
                conn.rollback()
                conn.commit()
                cur.close()
                await ctx.send("Translation already exists, or you fucking broke the bot. Congrats, asshole.")

    @commands.command(name='remove_peachlator', help='Removes a translation')
    async def remove_peachlator(self, ctx, *, key: str):
        if_MIA = await check_server(ctx)
        if if_MIA:
            # Even more SQL
            cur = conn.cursor()
            sql = """SELECT input, output FROM peachdict;"""
            cur.execute(sql)
            row = cur.fetchone()
            while row is not None:
                if row[0] == key:
                    sql = f"""DELETE FROM peachdict WHERE input='{key}';"""
                    cur.execute(sql)
                    conn.commit()
                    await ctx.send("Removal successful.")
                    break
                row = cur.fetchone()
            else:
                await ctx.send("Translation doesn't exist.")

            cur.close()

    @commands.command(name='madlibs', helps="Replaces word types encased in square brackets with random words")
    async def madlibs(self, ctx, *, msg: str):
        # A dict to convert word type aliases to the actual word type
        wordalias = {'noun' : 'noun',
                     'n': 'noun',
                     'verb': 'verb',
                     'v': 'verb',
                     'adverb': 'adverb',
                     'adv': 'adverb',
                     'adjective': 'adjective',
                     'adj': 'adjective'}

        # Regex to detect anything in between square brackets
        pattern = re.compile('\[(.*?)\]')
        if not pattern.findall(msg):
            return await ctx.send("No words to swap given. Enclose a valid word type in square brackets, "
                                  "like ``[noun]``.")

        output = ""
        prev = 0
        iterator = pattern.finditer(msg)

        try:
            for match in iterator:
                # good luck trying to figure this out in three years
                output += msg[prev:match.span()[0]] + random.choice(WORDS[(wordalias[match.group()[1:-1]])])
                prev = match.span()[1]
            output += msg[prev:]

            await ctx.send(output)
        except KeyError as e:
            await ctx.send(f"No idea what ``{e.args[0]}`` is. Valid word types are ``noun`` (``n``), ``verb`` (``v``), "
                           f"``adjective`` (``adj``), and ``adverb`` (``adv``).")

def setup(bot):
    bot.add_cog(Basic(bot))