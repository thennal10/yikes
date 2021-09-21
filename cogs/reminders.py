import os
import re
import time
import calendar
import asyncio
import psycopg2
import googleapiclient.discovery
from datetime import datetime
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']
YOUTUBE_KEY = os.environ['YOUTUBE_KEY']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

class Reminders(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='remindme',
                      aliases=['rm'],
                      usage="$remindme [message] in [time] [quantity] [time] [quantity]...")
    async def remindme(self, ctx, *, input):
        """Reminds you after a specified delay"""

        split_input = input.split(' in ')
        if len(split_input) == 1:  # input checking
            # check if it's a youtube URL
            url_pattern = re.compile('https?:\/\/(www\.)?(youtube|youtu.be)(.com)?\/(watch\?v=)?(.+?)(?=[&?\s]|$)')
            match = url_pattern.match(input)

            if match:
                youtube_id = match.groups()[-1]
                youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_KEY)

                request = youtube.videos().list(part="liveStreamingDetails", id=youtube_id)
                response = request.execute()

                try:
                    time_utc = response['items'][0]['liveStreamingDetails']['scheduledStartTime']
                    time_unix = calendar.timegm(time.strptime(time_utc, '%Y-%m-%dT%H:%M:%SZ'))

                    wait_time = time_unix - time.time()
                    content = input
                except:
                    raise commands.UserInputError("Invalid youtube url, or not an upcoming premiere/livestream.")
            else:
                raise commands.UserInputError('Invalid arguments.')
        else: # no error
            # Makes life easier
            time_conv = {'second': 1,
                         'minute': 60,
                         'hour': 3600,
                         'day': 86400,
                         'week': 604800}
            time_conv.update({k + 's': time_conv[k] for k in time_conv})  # Just adds plural versions

            content = " in ".join(split_input[:-1])  # Rejoins any split up 'in's in the message

            # calculates the time delay
            wait_time = 0
            time_unparsed = split_input[-1].split(' ')
            for i, word in enumerate(time_unparsed):
                if word in time_conv.keys():
                    multiplier = int(time_unparsed[i - 1])
                    wait_time += multiplier * time_conv[word]

            if wait_time <= 0:  # more input error checking
                raise commands.UserInputError('Invalid time.')

            time_unix = time.time() + wait_time

        # add the reminder to the database, w unix time
        sql = f"""INSERT INTO reminders VALUES ({ctx.message.author.id}, '{content}', {int(time_unix)});"""
        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            cur.close()
            readable_time = datetime.utcfromtimestamp(time_unix).strftime('%d/%m/%Y, %H:%M:%S')
            await ctx.send(f"Reminder set for {readable_time}")
        except Exception as e:
            conn.rollback()
            conn.commit()
            cur.close()
            await ctx.send(f"Error: ``{e}``")

        await self.reminder(wait_time, ctx.author, content)  # set reminder

    @commands.command(name='reminderlist', aliases=['rlist'])
    async def reminderlist(self, ctx):
        """Lists all upcoming reminders"""

        sql = """SELECT user_id, message, time FROM reminders;"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        listoutput = ""
        while row is not None:
            if row[0] == ctx.author.id:
                listoutput += f"""{datetime.utcfromtimestamp(row[2]).strftime('%d/%m/%Y, %H:%M:%S')} | {row[1]}\n"""
            row = cur.fetchone()
        cur.close()
        if not listoutput:
            return await ctx.send('You have no reminders set.')
        await ctx.send("**Your Reminders**\n```" + listoutput + "```")

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

        table.sort(key = lambda x: x[2]) # sort the table by time
        for row in table:  # (user_id, message, unix time)
            user = await self.bot.fetch_user(row[0])
            if row[2] <= time.time():
                await self.del_and_send(user, row[1])
            else:
                await self.reminder(row[2] - time.time(), user, row[1])


def setup(bot):
    bot.add_cog(Reminders(bot))
