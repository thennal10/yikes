from discord.ext import commands


class SourceCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 635538705389584425:
            try:
                msg = message.content.split(" ")
                output_channel = self.bot.get_channel(int(msg[0]))
                await output_channel.send(" ".join(msg[1:]))
            except ValueError:
                await message.channel.send("The first word of the message should be the channel ID.")
            except AttributeError:
                await message.channel.send("Can't find a channel with the given ID.")
        elif message.author.id == 453714878645927936 and message.content == "<:chibiaqua:611916034290614283>":
            posts = await message.channel.history(limit=2).flatten()
            delta = (message.created_at - posts[1].created_at)
            seconds = delta.seconds + (delta.days * 86400)
            hour = round(seconds / 3600)
            if hour > 1:
                await message.channel.send(f"Fire, posting a singular <:chibiaqua:611916034290614283> {hour} hours after"
                                           f" the conversation ended does not count as contributing to it.")


def setup(bot):
    bot.add_cog(SourceCog(bot))
