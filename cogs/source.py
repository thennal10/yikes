import os
import re
import random
import asyncio
import requests
import psycopg2
from discord.ext import commands

DATABASE_URL = os.environ['DATABASE_URL']
SAUCENAO_KEY = os.environ['SAUCENAO_KEY']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


class Source(commands.Cog):

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

    async def get_sauce(self, message):
        """Gets the actual sauce from message attachments"""
        urls = set()
        for attachment in message.attachments:
            img_url = attachment.url
            params = {"url": img_url, "output_type": 2, "db": 999, "api_key": SAUCENAO_KEY}

            max_attempts = 5
            attempts = 0

            while attempts < max_attempts:
                # Make a request to saucenao api
                rq = requests.get("https://saucenao.com/search.php", params=params)
                sauce = rq.json()

                # If not rate limited, break out of while loop and continue with the rest of the code
                if sauce['header']['status'] != -2:
                    break

                # If rate limited, wait and try again
                await asyncio.sleep(30 + random.randrange(30))
                attempts = attempts + 1
            else:
                return

            results = sauce['results']

            # check for minimum similarity requirement
            def similarity_check(r): return float(r['header']['similarity']) > 80
            # try and find a pixiv link that passes similarity check
            for result in results:
                try: pixiv_check = 'www.pixiv.net' in result['data']['ext_urls'][0]
                except: continue

                if similarity_check(result) and pixiv_check:
                    urls.add(result['data']['ext_urls'][0])
                    break
            # if no pixiv link, just get the first result and see if it passes the sim check
            else:
                if similarity_check(results[0]):
                    urls.add(results[0]['data']['ext_urls'][0])
        return urls

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in self.active_channels:
            match = re.search(r'https://(www\.)?pixiv\.net/(en/)?artworks/(\d*)(/\d*)?', message.content)
            if match and not message.attachments:
                id = match.group(3)
                try:
                    picn = match.group(4)[1:]
                except TypeError:
                    picn = 0
                await message.reply(f'https://api.pixiv.moe/image/{id}-{picn}.png')
            elif not match and message.attachments:
                urls = await self.get_sauce(message)
                if urls:
                    await message.reply("\n".join([f'<{url}>' for url in urls]))

    @commands.command(name='sauce')
    async def sauce(self, ctx):
        """Sauces attached images"""
        urls = await self.get_sauce(ctx.message)
        if len(urls):
            await ctx.reply("\n".join([f'<{url}>' for url in urls]))
        else:
            await ctx.reply('No sauce found for attached images, or no attached images found.')

    @commands.command(name='sauce_activate', brief='Activates saucing')
    async def sauce_activate(self, ctx):
        """Activates automatic pixiv source finding for the posted channel"""
        # SQL shit
        sql = """INSERT INTO saucechan (channel) VALUES (%s);"""
        data = (ctx.channel.id,)
        print(data)
        cur = conn.cursor()
        try:
            cur.execute(sql, data)
            conn.commit()
            cur.close()
            await ctx.send("Saucing activated for this channel.")
            self.update()
        except Exception as e:
            print(e)
            conn.rollback()
            conn.commit()
            cur.close()
            await ctx.send("Channel is already sauced up.")

    @commands.command(name='sauce_deactivate')
    async def sauce_deactivate(self, ctx):
        """Deactivates saucing"""
        # Even more SQL
        sql = """SELECT channel FROM saucechan;"""
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        while row is not None:
            if row[0] == ctx.channel.id:
                sql = f"""DELETE FROM saucechan WHERE channel ='{ctx.channel.id}';"""
                cur.execute(sql)
                conn.commit()
                await ctx.send("Deactivation successful. No more sauce for this channel.")
                self.update()
                break
            row = cur.fetchone()
        else:
            await ctx.send("Channel isn't sauced to begin with.")
        cur.close()

    @commands.command(name="trace")
    async def trace(self, ctx, url: str = None):
        """Finds the source of an anime screenshot"""
        if url:
            await ctx.reply(tracer(url))
        else:
            if len(ctx.message.attachments) == 0:
                raise commands.UserInputError('Missing image url or an attachment.')
            for attachment in ctx.message.attachments:
                await ctx.reply(tracer(attachment.url))


def tracer(url):
    req = requests.get(url="https://trace.moe/api/search?", params={"url": url})

    if req.status_code != 200:  # quick check for url validity
        return "The linked url/attachment was invalid."

    result = req.json()['docs'][0]
    output = f"{round(result['similarity'] * 100)}% sure that it's from **{result['title_romaji']}**"
    if result['episode']:
        output += f", EP {result['episode']}"

    return output + f"\nhttps://anilist.co/anime/{result['anilist_id']}"


def setup(bot):
    bot.add_cog(Source(bot))
