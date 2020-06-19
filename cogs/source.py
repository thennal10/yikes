import requests
from discord.ext import commands
import logging
from saucenao import SauceNao


saucenao = SauceNao(directory='data', databases=999, minimum_similarity=65, combine_api_types=False,
                    api_key='', exclude_categories='', move_to_categories=False,  use_author_as_category=False,
                    output_type=SauceNao.API_HTML_TYPE, start_file='', log_level=logging.ERROR,
                    title_minimum_similarity=90)


class Source(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 413449617401708555:
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
