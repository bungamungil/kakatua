from discord.ext import commands
import env
import kakatua

bot = commands.Bot(command_prefix=commands.when_mentioned_or(env.cmd_prefix))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    print(message)
    await bot.process_commands(message)


bot.add_cog(kakatua.Kakatua(bot))
bot.run(env.bot_token)
