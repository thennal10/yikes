import re
import asyncio
import discord
import youtube_dl
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=True))
        return await YTDLSource.generate(data)

    @classmethod
    async def from_search(cls, search, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{search}", download=True))
        return await YTDLSource.generate(data)

    @classmethod
    async def generate(cls, data):
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        bot.loop.create_task(self.audio_player_task())

    async def audio_player_task(self):
        while True:
            self.next.clear()
            current = await self.queue.get()
            self.ctx.voice_client.play(current, after = lambda e: self.next.set())
            await self.ctx.send(f"Now playing: `{current.data['title']}`")
            await self.next.wait()

    @commands.command(name='join')
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(name='play', aliases=['p', 'pl'])
    async def play(self, ctx, *, inp):
        """Plays from a url (almost anything youtube_dl supports)"""

        url_pattern = re.compile('https?:\/\/(www\.)?(youtube|youtu.be)(.com)?\/(watch\?v=)?(.+?)(?=[&?\s]|$)')
        match = url_pattern.match(inp)

        async with ctx.typing():
            if match:
                player = await YTDLSource.from_url(inp, loop=self.bot.loop)
            else:
                player = await YTDLSource.from_search(inp, loop=self.bot.loop)
            await self.queue.put(player)

        await ctx.send(f'Added to queue: `{player.title}`')

    @commands.command(name='queue', aliases=['q'])
    async def list_queue(self, ctx):
        """Lists the current music queue"""

        output = '\n'.join([element.data['title'] for element in self.queue._queue])
        await ctx.send(f"**Next Up**\n```{output}```")

    @commands.command(name='skip', aliases=['s'])
    async def skip(self, ctx):
        """Skips the current song and continues to the next in queue"""

        ctx.voice_client.stop()
        await ctx.send("Skipped currently playing song.")

    @commands.command(name='clear', aliases=['cl'])
    async def clear(self, ctx):
        """Clears the music queue"""

        self.queue = asyncio.Queue()
        await ctx.send("Cleared queue.")

    @commands.command(name='volume', aliases=['v'])
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%.")

    @commands.command(name='disconnect', aliases=['dc', 'fuckoff'])
    async def disconnect(self, ctx):
        """Stops and disconnects the bot from voice"""

        self.queue = asyncio.Queue()
        await ctx.voice_client.disconnect()

    # Are there better ways to do this? Probably. Will I dig up said better ways
    # and refactor this to not be shit? Absolutely not.
    @play.before_invoke
    @list_queue.before_invoke
    @skip.before_invoke
    @clear.before_invoke
    @volume.before_invoke
    @disconnect.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                self.ctx = ctx
            else:
                raise commands.UserInputError("You are not connected to a voice channel.")


def setup(bot):
    bot.add_cog(Music(bot))