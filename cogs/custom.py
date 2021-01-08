import os
import traceback
import sys
import psycopg2
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


class Custom(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Doubles as an error handler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.reply(f'{error}\nType `$help {ctx.command.name}` for usage instructions.')

        elif isinstance(error, commands.CheckFailure):
            await ctx.reply(error)

        elif isinstance(error, commands.CommandNotFound):
            # More SQL shit
            sql = """SELECT command, output FROM customcommands;"""
            cur = conn.cursor()
            cur.execute(sql)
            row = cur.fetchone()

            while row is not None:
                if row[0] == ctx.invoked_with:
                    cur.close()
                    return await ctx.send(row[1])
                row = cur.fetchone()
            else:
                await ctx.reply(f'Command `${ctx.invoked_with}` not found.')

        else:
            print(error)
            await ctx.reply('Something went wrong. Ping Premed and tell him to fix his bot.')

    @commands.command(name='custom', help='Adds a custom command')
    @commands.is_owner()
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
        except Exception as e:
            print(e)
            conn.rollback()
            conn.commit()
            cur.close()
            await ctx.send("Command already exists, or you fucking broke the bot. Congrats, asshole.")

    @commands.command(name='remove', help='Removes a custom command')
    @commands.is_owner()
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
                conn.commit()
                await ctx.send("Removal successful.")
                break
            row = cur.fetchone()
        else:
            await ctx.send("That command doesn't exist, you dumb fuck. Use ``$list`` to get a list of existing"
                           " commands.")
        cur.close()

    @commands.command(name='list', help='Lists all custom commands')
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
    bot.add_cog(Custom(bot))
