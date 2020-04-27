from discord.ext import commands


class Specific(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 635538705389584425 and message.author.id == 293716762636320768:
            try:
                msg = message.content.split(" ")
                output_channel = self.bot.get_channel(int(msg[0]))
                await output_channel.send(" ".join(msg[1:]))
            except ValueError:
                await message.channel.send("The first word of the message should be the channel ID.")
            except AttributeError:
                await message.channel.send("Can't find a channel with the given ID.")

def setup(bot):
    bot.add_cog(Specific(bot))
