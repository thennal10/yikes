import os
import requests
import wikipedia
from discord import Embed
from discord.ext import commands
from jikanpy import Jikan

jikan = Jikan()
vglist_token = os.environ['VGLIST_TOKEN']
vglist_email = os.environ['VGLIST_EMAIL']

class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime', help='Pulls up the mal and anilist of a given anime')
    async def anisearch(self, ctx, *, search):
        # Temp fix until mal gets its shit back together
        #search_result = jikan.search('anime', search)
        #title = search_result['results'][0]['title']
        #result_url = search_result['results'][0]['url']

        query = '''
        query ($search: String) {
            Media (search: $search, type: ANIME) {
                id
            }
        }
        '''
        variables = {
            'search': search
        }
        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})
        if response:
            # convert the response to a dict using json() and get the id
            anime_id = response.json()['data']['Media']['id']
            await ctx.send(f"https://anilist.co/anime/{anime_id}")
        else:
            await ctx.send(f"Anilist URL not found")

    @anisearch.error
    async def anisearch_error(self, ctx, error):
        print(error)
        await ctx.send("Usage: ``$anime [search]``")


    @commands.command(name='manga', help='Pulls up the mal and anilist of a given manga/ln')
    async def mangasearch(self, ctx, *, search):
        # See above
        #search_result = jikan.search('manga', search)
        #title = search_result['results'][0]['title']
        #result_url = search_result['results'][0]['url']

        query = '''
        query ($search: String) {
            Media (search: $search, type: MANGA) {
                id
            }
        }
        '''
        variables = {
            'search': search
        }
        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})

        if response:
            # convert the response to a dict using json() and get the id
            manga_id = response.json()['data']['Media']['id']
            await ctx.send(f"https://anilist.co/manga/{manga_id}")
        else:
            await ctx.send(f"Anilist URL not found")

    @mangasearch.error
    async def mangasearch_error(self, ctx, error):
        print(error)
        await ctx.send("Usage: ``$manga [search]``")


    @commands.command(name='game', help='Pulls up the vglist link for a given game')
    async def gamesearch(self, ctx, *, search):
        query = '''
                query($query: String!) {
                  gameSearch(query: $query) {
                    nodes {
                      id
                      name
                      coverUrl
                    }
                  }
                }
                '''
        variables = {'query': search}
        headers = {
            "User-Agent": "Yikes",
            "X-User-Token": vglist_token,
            "X-User-Email": vglist_email,
            "Content-Type": "application/json",
            "Accept": "*/*"
        }
        url = 'https://vglist.co/graphql'

        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers).json()

        results = response['data']['gameSearch']['nodes']
        if len(results) == 0:
            await ctx.send(f"Game not found.")
        else:
            await ctx.send(f"https://vglist.co/games/{results[0]['id']}")

    @gamesearch.error
    async def gamesearch_error(self, ctx, error):
        print(error)
        await ctx.send("Usage: ``$game [search]``")


    @commands.command(name='wiki', help='Pulls up the wikipedia link for a given search')
    async def wikisearch(self, ctx, *, search):
        results = wikipedia.search(search)
        if len(results) == 0:
            return await ctx.send(f"No results found for ``{search}``")
        await ctx.send(wikipedia.page(results[0]).url)

    @wikisearch.error
    async def wikisearch_error(self, ctx, error):
        print(error)
        await ctx.send("Usage: ``$wiki [search]``")


    @commands.command(name='urban', help='Pulls up the urban dictionary entry for a given search')
    async def urban(self, ctx, *, search):
        request = requests.get("http://api.urbandictionary.com/v0/define", params={"term": search})

        try:
            result = request.json()['list'][0]

            # Makes a nice looking embed
            embed = Embed(title=f"**{result['word']}** by {result['author']}", description=f"{result['definition']}", color=0xb3c98d)
            embed.add_field(name="Example(s)", value=result['example'], inline=False)
            embed.add_field(name="Thumbs", value=f":thumbsup:{result['thumbs_up']} | :thumbsdown:{result['thumbs_down']}", inline=False)
            embed.add_field(name="Link", value=result['permalink'])

            await ctx.send(embed=embed)
        except IndexError:
            await ctx.send(f"Nothing found for ``{search}``.")

    @urban.error
    async def urban_error(self, ctx, error):
        print(error)
        await ctx.send("Usage: ``$urban [search]``")

def setup(bot):
    bot.add_cog(Search(bot))