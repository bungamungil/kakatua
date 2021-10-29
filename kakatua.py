from discord.ext import commands
from ytdl.source import YTDLSource


class Kakatua(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def check(self, ctx: commands.Context, *, text):
        await ctx.send(text)

    @commands.command()
    async def play(self, ctx: commands.Context, *, url):
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {player.title}')

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
