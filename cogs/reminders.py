import os
import time
import datetime
import asyncio
import psycopg2
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

class Reminders(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reminder_error_message = "Usage: ``$remindme [message] in [time] [quantity] [time] [quantity]...``\n" \
                                      + "Eg: ``$remindme simp for coco in 2 weeks 3 hours 1 second``"

    @commands.command(name='remindme', help='Reminds you after a specified delay')
    async def remindme(self, ctx, *, input):
        # Makes life easier
        time_conv = {'second': 1,
                     'minute': 60,
                     'hour': 3600,
                     'day': 86400,
                     'week': 604800}
        time_conv.update({k + 's':time_conv[k] for k in time_conv}) # Just adds plural versions

        split_input = input.split(' in ')
        if len(split_input) == 1: # input error checking
            return await ctx.send(self.reminder_error_message)

        content = " in ".join(split_input[:-1]) # Rejoins any split up 'in's in the message

        # calculates the time delay
        wait_time = 0
        time_unparsed = split_input[-1].split(' ')
        for i, word in enumerate(time_unparsed):
            if word in time_conv.keys():
                multiplier = int(time_unparsed[i - 1])
                wait_time += multiplier * time_conv[word]

        if wait_time <= 0: # more input error checking
            return await ctx.send(self.reminder_error_message)

        # add the reminder to the database, w unix time
        sql = f"""INSERT INTO reminders VALUES ({ctx.message.author.id}, '{content}', {int(time.time() + wait_time)});"""
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            cur.close()
            readable_time = datetime.datetime.utcfromtimestamp(time.time() + wait_time).strftime('%d/%m/%Y, %H:%M:%S')
            await ctx.send(f"Reminder set for {readable_time}")
        except Exception as e:
            conn.rollback()
            conn.commit()
            cur.close()
            await ctx.send(f"Error: ``{e}``")

        await self.reminder(wait_time, ctx.author, content) # set reminder

    @remindme.error
    async def remindme_error(self, ctx, error):
        await ctx.send(self.reminder_error_message)

    # sleeps for a while and then calls another function
    async def reminder(self, seconds, ctx, content):
        await asyncio.sleep(seconds)
        await self.del_and_send(ctx, content)

    # deletes the reminder from the database and sends it to the recipient
    async def del_and_send(self, ctx, content):
        # Remove the reminder from the database
        sql = f"""DELETE FROM reminders WHERE message='{content}';"""
        cur = conn.cursor()

        try:
            cur.execute(sql)
            conn.commit()
            cur.close()
            await ctx.send(content)
        except Exception as e:
            conn.rollback()
            conn.commit()
            cur.close()
            await ctx.send(f"Reminder Error: ``{e}``")

    # check for, set, and send reminders on startup
    @commands.Cog.listener()
    async def on_ready(self):
        sql = f"""SELECT * FROM reminders"""
        cur = conn.cursor()
        cur.execute(sql)
        table = cur.fetchall()

        for row in table: # (user_id, message, unix time)
            user = self.bot.get_user(row[0])
            if row[2] <= time.time():
                await self.del_and_send(user, row[1])
            else:
                await self.reminder(row[2] - time.time(), user, row[1])

def setup(bot):
    bot.add_cog(Reminders(bot))
