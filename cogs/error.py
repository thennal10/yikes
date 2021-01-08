import os
from discord.ext import commands

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.reply(f'{error}\nType `$help {ctx.command.name}` for usage instructions.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.reply(error)
        else:
            print(error)
            await ctx.reply('Something went wrong. Ping Premed and tell him to fix his bot.')
def setup(bot):
    bot.add_cog(ErrorHandler(bot))