from discord.ext import commands


def leaderboard_name(l):
    name = ""
    for count, element in enumerate(l):
        name += element.capitalize()
        if count != len(l) - 1:
            name += "/"
    return name


class Basic(commands.Cog):
    """BasicCog"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='strokify', help='TuRnS gIvEn InPuT tO tHiS')
    async def strokify(self, ctx, *, input: str):

        iscap = False
        outputmsg = list(input)
        for count, character in enumerate(outputmsg):
            if character.isalpha():
                if iscap:
                    outputmsg[count] = character.capitalize()
                iscap = not iscap

        await ctx.send("".join(outputmsg))

    @strokify.error
    async def strokify_error(self, ctx, error):
        await ctx.send("Usage: ``!strokify [phrase]``")


    @commands.command(name='score', help='Outputs a score based on the string')
    async def score(self, ctx, *, input: str):

        num = 0
        for character in input:
            num += ord(character)
        num = (num % 10) + 1

        await ctx.send(f"bout {num}/10")

    @score.error
    async def score_error(self, ctx, error):
        await ctx.send("Usage: ``!score [phrase]``")


    @commands.command(name='leaderboard', help='Creates a leaderboard based on a given word/phrase')
    async def word_leaderboard(self, ctx, msglimit: int, *, actmsg: str):

        searchwords = actmsg.split(" + ")
        print(searchwords)
        peeps = [["N/A", 0]]

        for chan in ctx.guild.text_channels:
            perm = chan.permissions_for(ctx.guild.me)
            if perm.read_message_history:
                async for msg in chan.history(limit=msglimit):
                    for searchword in searchwords:
                        if searchword in msg.content.lower() and not msg.author.bot:
                            found = 0
                            for peep in peeps:
                                if msg.author.name == peep[0]:
                                    peep[1] += 1
                                    found = 1
                                    break
                            if found == 0:
                                peeps.append([msg.author.name, 1])
            print(chan)
        peeps.sort(key=lambda x:x[1], reverse=True)

        leaderboard = f"**The {leaderboard_name(searchwords)} Leaderboard**```\nRank  | Name\n\n"
        for count, peep in enumerate(peeps[:10]):
            leaderboard += f"""[{count + 1}]   > {peep[0]}: {peep[1]}\n"""
        leaderboard += "```"
        await ctx.send(leaderboard)

    @word_leaderboard.error
    async def word_leaderboard_error(self, ctx, error):
        print(error)
        await ctx.send("Usage: ``!leaderboard [no of messages] [phrase1] + [phrase2]...``")


    @commands.command(name='peachlator', help='What it says on the tin')
    async def peachlator(self, ctx, *, inp: str):
        # load dict
        trans_dict = {'winky babies': 'sperm',
                      'winky': 'penis',
                      'winkies': 'penises',
                      'hooha': 'vagina',
                      'hoohas': 'vaginas',
                      'poot': 'flatulate',
                      'poots': 'flatulence',
                      'spawn': 'baby',
                      'babies': 'semen',
                      'baby': 'sperm cell',
                      'boys': 'testicles',
                      'boy': 'testicle',
                      'horizontal festivity': 'sexual intercourse',
                      'horizontal festivities': 'sexual intercourse',
                      'horizontal stuff': 'sexual intercourse',
                      'penguindrum': 'trash',
                      'wotakoi': 'trash',
                      'nether region': 'genital area',
                      'nether regions': 'genital areas',
                      'jellybean': 'clitoris',
                      'jellybeans': 'clitorides',
                      'jellybeanmegaly': 'clitoromegaly',
                      'mother nature time': 'menstruation'}

        # made it into a list so I don't have to worry about differing word lengths
        new_message = ["Translation:"] + inp.split()

        # new dict with keys as a list of words
        flattened_dict = {tuple(k.split()): trans_dict[k] for k in trans_dict}

        for key in flattened_dict:
            # indicates the point we're at with the given key
            i = 0
            caps = False
            allcaps = False
            for idx, word in enumerate(new_message):
                if (key[i] == word) or (key[i] == word.lower()):

                    # check if the word is capitalized or in allcaps
                    if key[i].capitalize() == word:
                        caps = True
                    if key[i].upper() == word:
                        allcaps = True

                    i += 1
                    # if we find a valid word
                    if i == len(key):

                        if caps:
                            result = flattened_dict[key].capitalize()
                        elif allcaps:
                            result = flattened_dict[key].upper()
                        else:
                            result = flattened_dict[key]

                        new_message[idx] = result
                        # remove leftover words
                        for r in range(1, i):
                            new_message.pop(idx - r)

                        i = 0

                else:
                    # so that it's a continuous word and not like, splintered across a sentence
                    i = 0
                    caps = False
                    allcaps = False

        await ctx.send(" ".join(new_message))

    @peachlator.error
    async def peachlator_error(self, ctx, error):
        await ctx.send("Peachlator, at your service. Usage: ``!peachlator [text]``")


def setup(bot):
    bot.add_cog(Basic(bot))