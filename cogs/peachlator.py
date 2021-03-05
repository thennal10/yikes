import os
import psycopg2
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


class Peachlator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='peachlator', usage='$peachlator [text] OR reply to message')
    async def peachlator(self, ctx):
        """Translates to peachlang"""
        # get the table
        cur = conn.cursor()
        sql = """SELECT * FROM peachdict;"""
        cur.execute(sql)
        table = cur.fetchall()
        cur.close()

        # check for replies first, then move on to text included with command
        ref = ctx.message.reference
        if ref:
            message_split = ref.resolved.content.split()
        else:
            message_split = ctx.message.content.split()[1:]
            if not message_split:
                raise commands.UserInputError('No reply or text to translate found.')
        new_message = ["Translation:"] + message_split

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

    @commands.command(name='update_peachlator', usage='$update_peachlator [word] - [translation]')
    @commands.is_owner()
    async def update_peachlator(self, ctx, *, inp: str):
        """Update the peachlator. Premed only"""
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
        except Exception as e:
            print(e)
            conn.rollback()
            conn.commit()
            cur.close()
            await ctx.send("Translation already exists, or you fucking broke the bot. Congrats, asshole.")

    @commands.command(name='remove_peachlator')
    @commands.is_owner()
    async def remove_peachlator(self, ctx, *, key: str):
        """Removes a translation. Premed only"""
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


def setup(bot):
    bot.add_cog(Peachlator(bot))