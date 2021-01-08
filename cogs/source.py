import os
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
        self.short_limit = 6

    def update(self):
        sql = """SELECT channel FROM saucechan;"""
        cur = conn.cursor()
        cur.execute(sql)
        self.active_channels = [tup[0] for tup in cur.fetchall()]
        cur.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in self.active_channels:
            if "source" not in message.content.lower():
                urls = set()
                for attachment in message.attachments:
                    img_url = attachment.url
                    params = {"url": img_url, "output_type": 2, "db": 999, "api_key": SAUCENAO_KEY}

                    # because saucenao rate limiting
                    if self.short_limit <= 1:
                        loop_count = 0
                        while self.short_limit <= 1 and loop_count < 10:
                            loop_count += 1 # a failsafe to prevent an infinitely running loop
                            await asyncio.sleep(30)

                            # check (and assign vars) if you've hit the cap, because commands are async
                            rq = requests.get("https://saucenao.com/search.php", params=params)
                            sauce = rq.json()
                            try:
                                self.short_limit = sauce['header']['short_remaining']
                                break
                            except KeyError:
                                if sauce['header']['status'] == -2:
                                    continue
                                else:
                                    raise Exception(f'Saucenao request failed. Request: {sauce}')
                    else: # an if else so that it doesn't request twice
                        rq = requests.get("https://saucenao.com/search.php", params=params)
                        sauce = rq.json()
                        self.short_limit = sauce['header']['short_remaining']

                    results = sauce['results']

                    for result in results:
                        similarity_check = float(result['header']['similarity']) > 80
                        try:
                            pixiv_check = 'www.pixiv.net' in result['data']['ext_urls'][0]
                        except:
                            continue
                        if similarity_check and pixiv_check:
                            urls.add(result['data']['ext_urls'][0])
                            break
                    else:
                        if float(results[0]['header']['similarity']) > 80:
                            urls.add(results[0]['data']['ext_urls'][0])
                if len(urls):
                    await message.reply("\n".join([f'<{url}>' for url in urls]))

    @commands.command(name='sauce_activate', help='Activates automatic pixiv source finding for the posted channel')
    async def sauce_activate(self, ctx):
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
        except:
            conn.rollback()
            conn.commit()
            cur.close()
            await ctx.send("Channel is already sauced up.")

    @sauce_activate.error
    async def sauce_activate_error(self, ctx, error):
        await ctx.send("Something went wrong. REEEE at premed.")

    @commands.command(name='sauce_deactivate', help='Deactivates saucing.')
    async def sauce_deactivate(self, ctx):
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

    @sauce_deactivate.error
    async def sauce_deactivate_error(self, ctx):
        await ctx.send("Something went wrong. REEE at premed.")


    @commands.command(name="trace", help="Finds the source of an anime screenshot")
    async def trace(self, ctx, url: str = None):
        if url:
            await ctx.reply(self.tracer(url))
        else:
            for attachment in ctx.message.attachments:
                await ctx.reply(self.tracer(attachment.url))

    def tracer(self, url):
        req = requests.get(url="https://trace.moe/api/search?", params={"url": url})

        if req.status_code != 200:  # quick check for url validity
            return "The linked url/attachment was invalid"

        result = req.json()['docs'][0]
        output = f"{round(result['similarity'] * 100)}% sure that it's from **{result['title_romaji']}**"
        if result['episode']:
            output += f", EP {result['episode']}"

        return output + f"\nhttps://anilist.co/anime/{result['anilist_id']}"

    @trace.error
    async def trace_error(self, ctx, error):
        await ctx.send("Usage: ``$trace [image url]`` or just ``$trace`` with an image attachment")


def setup(bot):
    bot.add_cog(Source(bot))
