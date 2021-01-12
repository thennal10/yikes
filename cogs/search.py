import os
import requests
from discord import Embed
from discord.ext import commands

vglist_token = os.environ['VGLIST_TOKEN']
vglist_email = os.environ['VGLIST_EMAIL']


class Search(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime', help='Pulls up the anilist of a given anime.')
    async def anisearch(self, ctx, *, search):
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
            await ctx.reply(f"https://anilist.co/anime/{anime_id}")
        else:
            await ctx.reply(f"Anilist URL not found")

    @commands.command(name='manga', help='Pulls up the anilist of a given manga/ln.')
    async def mangasearch(self, ctx, *, search):
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
            await ctx.reply(f"https://anilist.co/manga/{manga_id}")
        else:
            await ctx.reply(f"Anilist URL not found")

    @commands.command(name='game', help='Pulls up the vglist link for a given game.')
    async def gamesearch(self, ctx, *, search):
        query = '''
                query($query: String!) {
                  gameSearch(query: $query) {
                    nodes {
                      id
                      steamAppIds
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
            await ctx.reply(f"Game not found.")
        else:
            output = f"https://vglist.co/games/{results[0]['id']}"
            if len(results[0]['steamAppIds']):
                output += f"\nhttps://store.steampowered.com/app/{results[0]['steamAppIds'][0]}"
            await ctx.reply(output)

    @commands.command(name='wiki', help='Pulls up the wikipedia link for a given search.')
    async def wikisearch(self, ctx, *, search):
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": search,
            "prop": "info",
            "inprop": "url"
        }

        req = requests.get(url="https://en.wikipedia.org/w/api.php", params=params)

        try:
            result = req.json()['query']['pages']
            # it gives you an unsorted list by default, for some reason
            for r in result:
                if result[r]['index'] == 1:
                    return await ctx.reply(result[r]['fullurl'])
        except KeyError:
            await ctx.reply(f"Nothing found for ``{search}``.")

    @commands.command(name='urban', help='Pulls up the urban dictionary entry for a given search.')
    async def urban(self, ctx, *, search):
        request = requests.get("http://api.urbandictionary.com/v0/define", params={"term": search})

        try:
            result = request.json()['list'][0]

            # Makes a nice looking embed
            embed = Embed(title=f"**{result['word']}** by {result['author']}",
                          description=f"{parse(result['definition'])}",
                          color=0xb3c98d)
            embed.add_field(name="Example(s)",
                            value=parse(result['example']),
                            inline=False)
            embed.add_field(name="Thumbs",
                            value=f":thumbsup:{result['thumbs_up']} | :thumbsdown:{result['thumbs_down']}",
                            inline=False)
            embed.add_field(name="Link",
                            value=result['permalink'])

            await ctx.reply(embed=embed)
        except IndexError:
            await ctx.reply(f"Nothing found for ``{search}``.")

    @commands.command(name='rt', help='Pulls up the rotten tomatoes entry for a given search.')
    async def rt(self, ctx, *, search):
        rq = requests.get("https://www.rottentomatoes.com/api/private/v2.0/search", params={"q": search})
        try:
            result_url = rq.json()['movies'][0]['url']
            await ctx.reply("https://www.rottentomatoes.com" + result_url)
        except IndexError:
            await ctx.reply(f"Nothing found for ``{search}``.")


# just removes square brackets, used for $urban
def parse(word):
    return "".join([ch for ch in word if ch not in ['[', ']']])


def setup(bot):
    bot.add_cog(Search(bot))
