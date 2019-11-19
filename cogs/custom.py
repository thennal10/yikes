import os
import psycopg2
from discord.ext import commands


DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


class CustomCog(commands.Cog):
    """CustomCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='custom')
    async def custom_command(self, ctx, key, *, value):
        # SQL shit
        sql = """INSERT INTO customcommands (command, output) VALUES (%s, %s);"""
        data = (key, value)
        cur = conn.cursor()
        try:
            cur.execute(sql, data)
            conn.commit()
            cur.close()
            await ctx.send("Immortalized!")
        except:
            conn.rollback()
            conn.commit()
            cur.close()
            await ctx.send("Command already exists, or you fucking broke the bot. Congrats, asshole.")

    @custom_command.error
    async def custom_command_error(self, ctx, error):
        await ctx.send("Usage: ``!custom [command] [link/text]``")

    @commands.command(name='')
    async def call_command(self, ctx, key):
        # More SQL shit
        sql = """SELECT command, output FROM customcommands;"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        while row is not None:
            if row[0] == key:
                cur.close()
                await ctx.send(row[1])
            row = cur.fetchone()

    @commands.command(name='remove')
    async def remove(self, ctx, key):
        # Even more SQL
        sql = """SELECT command, output FROM customcommands;"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row is not None:
            if row[0] == key:
                sql = f"""DELETE FROM customcommands WHERE command ='{key}';"""
                cur.execute(sql)
                await ctx.send("Removal successful.")
                break
            row = cur.fetchone()
        else:
            await ctx.send("That command doesn't exist, you dumb fuck. Use ``list!`` to get a list of existing"
                           " commands.")
        cur.close()

    @remove.error
    async def remove_error(self, ctx, error):
        await ctx.send("Usage: ``!remove [command]``")

    @commands.command(name='list')
    async def cclist(self, ctx):
        # EVEN MORE SQL
        sql = """SELECT command, output FROM customcommands;"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        listoutput = "**List of Custom Commands**\n```"
        while row is not None:
            listoutput += f"""{row[0]}\n"""
            row = cur.fetchone()
        listoutput += "```"
        cur.close()
        await ctx.send(listoutput)


def setup(bot):
    bot.add_cog(CustomCog(bot))
