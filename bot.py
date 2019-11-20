import os
import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

# initializing shit
TOKEN = os.environ.get("TOKEN")


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    prefixes = ['!']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['cogs.basic', 'cogs.custom', 'cogs.search', 'cogs.source', 'cogs.tweet', 'cogs.generator',
                      'cogs.specific']

bot = commands.Bot(command_prefix=get_prefix, description='An abominable bot for an abominable server')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    await bot.change_presence(activity=discord.Activity(name='Yiking'))
    print(f'Successfully logged in and booted...!')


bot.run(TOKEN, bot=True, reconnect=True)
