import os
import discord
from discord.ext import commands

# initializing shit
TOKEN = os.environ.get("TOKEN")


def get_prefix(yikes, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    prefixes = ['$', 'y!']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(yikes, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = [f"cogs.{file.rstrip('.py')}" for file in os.listdir('./cogs') if file.endswith('.py')]

bot = commands.Bot(command_prefix=get_prefix,
                   description='An abominable bot for an abominable server',
                   allowed_mentions=discord.AllowedMentions(replied_user=False))

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

bot.run(TOKEN, bot=True, reconnect=True)
