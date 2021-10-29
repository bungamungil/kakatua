import discord
import env

intents = discord.Intents().all()
client = discord.Client(intents=intents)

client.run(env.bot_token)
