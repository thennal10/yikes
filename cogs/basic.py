from discord.ext import commands


def leaderboard_name(l):
    name = ""
    for count, element in enumerate(l):
        name += element.capitalize()
        if count != len(l) - 1:
            name += "/"
    return name


class BasicCog(commands.Cog):
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
        await ctx.send("Usage: ``!leaderboard [no of messages] [phrase1] + [phrase2]...``")


    @commands.command(name='peachlator', help='What it says on the tin')
    async def peachlator(self, ctx, *, input: str):
        # load dictionary
        trans_dict = {}
        file = open("peachdict.txt", "r")
        for line in file:
            isv = False
            value = ""
            key = ""
            for word in line.split():
                if word == "-":
                    isv = True
                elif isv:
                    strword = word.rstrip("\n")
                    value += strword + " "
                else:
                    key += word + " "
            trans_dict[key.rstrip()] = value.rstrip()

        # replace words
        new_message = ["Translation:"] + input.split()
        for i in range(len(new_message)):
            for key in trans_dict:
                splitkey = key.split()
                # don't ask
                for j, skey in enumerate(splitkey):
                    if i + j >= len(new_message):
                        incl = False
                        break
                    elif skey != new_message[i + j].lower():
                        incl = False
                        break
                    incl = True

                # Handles capitalization
                if new_message[i].isupper():
                    splitval = trans_dict[key].upper().split()
                elif new_message[i][0].isupper():
                    splitval = trans_dict[key].capitalize().split()
                else:
                    splitval = trans_dict[key].split()

                # still need to add a case for when splitval > splitkey but eh
                if incl:
                    for k, val in enumerate(splitval):
                        new_message[i + k] = val
                    for l in range((len(splitkey)) - (len(splitval))):
                        del new_message[i + l + len(splitval)]
                    i = i - len(splitval)

        await ctx.send(" ".join(new_message))

    @peachlator.error
    async def peachlator_error(self, ctx, error):
        await ctx.send("Peachlator, at your service. Usage: ``!peachlator [text]``")


    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Event Listener which is called when a user is banned from the guild."""

        print(f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(BasicCog(bot))