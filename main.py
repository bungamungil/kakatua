from discord.ext import commands
import env

bot = commands.Bot(command_prefix=commands.when_mentioned_or(env.cmd_prefix))


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


bot.run(env.bot_token)
