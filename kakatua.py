from discord.ext import commands
from ytdl.source import YTDLSource
from asyncio import sleep


class Kakatua(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.playlist = []
        self.player = None

    @commands.command()
    async def check(self, ctx: commands.Context, *, text):
        await ctx.send(text)

    @commands.command()
    async def play(self, ctx: commands.Context, *, url):
        self.playlist.extend(await YTDLSource.extract_info(url, loop=self.bot.loop, stream=True))
        await self.__play_next(ctx)

    @commands.command()
    async def stop(self, ctx: commands.Context):
        self.playlist.clear()
        if ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()

    @commands.command()
    async def np(self, ctx: commands.Context):
        await self.__display_current_playing(ctx)

    @commands.command()
    async def now_playing(self, ctx: commands.Context):
        await self.__display_current_playing(ctx)

    @play.before_invoke
    async def ensure_voice(self, ctx: commands.Context):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('You are not connected to a voice channel.')
                raise commands.CommandError('Author not connected to a voice channel.')
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    async def __play_next(self, ctx: commands.Context):
        if len(self.playlist) > 0:
            async with ctx.typing():
                data = self.playlist.pop(0)
                self.player = await YTDLSource.play_url(data, stream=True)
                ctx.voice_client.play(self.player, after=lambda e: print(f'Player error: {e}') if e else None)
                await self.__display_current_playing(ctx)
            while ctx.voice_client is not None and ctx.voice_client.is_playing():
                await sleep(1)
            await self.__play_next(ctx)
        elif ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

    async def __display_current_playing(self, ctx: commands.Context):
        await ctx.send(f'Now playing: {self.player.title}')
