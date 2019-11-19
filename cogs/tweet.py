import requests
from bs4 import BeautifulSoup
from discord.ext import commands


class TweetCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='expand')
    async def expand(self, ctx, url):

        if "twitter.com" not in url:
            await ctx.send("Not a link to a tweet.")
            return

        r = requests.get(url)

        soup = BeautifulSoup(r.content, 'html5lib')
        images_unparsed = soup.find_all("meta", {"property": "og:image"})

        if len(images_unparsed) == 1:
            await ctx.send("Tweet does not have any images or only has one image.")
            return

        output = ""
        for image in images_unparsed[1:]:
            output += f"{image['content']}\n"

        await ctx.send(output)

    @expand.error
    async def expand_error(self, ctx, error):
        await ctx.send("Usage: ``!expand [tweet]``")


def setup(bot):
    bot.add_cog(TweetCog(bot))
