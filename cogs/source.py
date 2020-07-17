import os
import requests
import psycopg2
from discord.ext import commands
import logging
from saucenao import SauceNao


DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
saucenao = SauceNao(directory='data', databases=999, minimum_similarity=65, combine_api_types=False,
                    api_key='', exclude_categories='', move_to_categories=False,  use_author_as_category=False,
                    output_type=SauceNao.API_HTML_TYPE, start_file='', log_level=logging.ERROR,
                    title_minimum_similarity=90)


class Source(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.update()

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
                for attachment in message.attachments:
                    img_data = requests.get(attachment.url).content

                    with open('data/temp.jpg', 'wb') as handler:
                        handler.write(img_data)

                    filtered_results = saucenao.check_file(file_name="temp.jpg")
                    if len(filtered_results) != 0:
                        for result in filtered_results:
                            try:
                                unparsed = result['data']['content'][0].split('\n')[0].split(" ")
                                for count, word in enumerate(unparsed):
                                    if word == "Pixiv":
                                        if unparsed[count + 1] == "ID:":
                                            pixiv_id = unparsed[count + 2]
                                        elif unparsed[count + 1][0] == "#":
                                            pixiv_id = unparsed[count + 1][1:]
                                await message.channel.send(f"Source: <https://www.pixiv.net/en/artworks/{pixiv_id}>")
                                break
                            except Exception as e:
                                print(e)

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
            await ctx.send(self.tracer(url))
        else:
            for attachment in ctx.message.attachments:
                await ctx.send(self.tracer(attachment.url))

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
