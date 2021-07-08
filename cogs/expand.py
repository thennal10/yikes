import os
import re
import psycopg2
import requests
from discord.ext import commands

TWITTER_TOKEN = os.environ['TWITTER_TOKEN']
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


class Expand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update()

    def update(self):
        """Update the active_channel property in memory"""
        sql = """SELECT channel FROM saucechan;"""
        cur = conn.cursor()
        cur.execute(sql)
        self.active_channels = [tup[0] for tup in cur.fetchall()]
        cur.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in self.active_channels:
            try:
                video = await self.tweet_expand(message.content)
                await message.reply(video)
            except Exception:
                pass

    async def tweet_expand(self, message):
        match = re.search(r'https:\/\/twitter\.com\/.*?\/status\/(\d*)', message)
        id = match.group(1)

        endpoint = "https://api.twitter.com/1.1/statuses/show.json"
        data = {
            "id": id,
            "include_entities": "true",
            "tweet_mode": "extended"
            }
        headers = {"Authorization": f"Bearer {TWITTER_TOKEN}"}

        max_attempts = 5
        attempts = 0

        while attempts < max_attempts:
            try:
                response = requests.get(endpoint, data=data, headers=headers).json()
                videos = response['extended_entities']['media'][0]['video_info']['variants']
                # get the url of the largest (read: last on the list) mp4 video
                video = [v for v in videos if v['content_type'] == 'video/mp4'][-1]['url']
                return video
            except Exception:
                attempts += 1



def setup(bot):
    bot.add_cog(Expand(bot))