import requests
from discord.ext import commands
from jikanpy import Jikan

jikan = Jikan()

class SearchCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime')
    async def anisearch(self, ctx, *, search):
        search_result = jikan.search('anime', search)
        title = search_result['results'][0]['title']
        result_url = search_result['results'][0]['url']

        query = '''
        query ($search: String) {
            Media (search: $search, type: ANIME) {
                id
            }
        }
        '''
        variables = {
            'search': title
        }
        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})
        if response:
            # convert the response to a dict using json() and get the id
            anime_id = response.json()['data']['Media']['id']
            await ctx.send(f"{result_url}\nhttps://anilist.co/anime/{anime_id}")
        else:
            await ctx.send(f"{result_url}\nAnilist URL not found")

    @anisearch.error
    async def anisearch_error(self, ctx, error):
        await ctx.send("Usage: ``!anime [search]``")


    @commands.command(name='manga')
    async def mangasearch(self, ctx, *, search):
        search_result = jikan.search('manga', search)
        title = search_result['results'][0]['title']
        result_url = search_result['results'][0]['url']

        query = '''
        query ($search: String) {
            Media (search: $search, type: MANGA) {
                id
            }
        }
        '''
        variables = {
            'search': title
        }
        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})

        if response:
            # convert the response to a dict using json() and get the id
            manga_id = response.json()['data']['Media']['id']
            await ctx.send(f"{result_url}\nhttps://anilist.co/manga/{manga_id}")
        else:
            await ctx.send(f"{result_url}\nAnilist URL not found")

    @mangasearch.error
    async def mangasearch_error(self, ctx, error):
        await ctx.send("Usage: ``!manga [search]``")


def setup(bot):
    bot.add_cog(SearchCog(bot))