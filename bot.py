import discord
import json
import os
from discord.ext import commands
from discord.ext.commands import has_permissions


intents = discord.Intents.default()
intents.members = True
intents.reactions = True

# load settings
with open('files/settings.json', 'r') as settings_file:
    settings_file = json.load(settings_file)
    PREFIX = settings_file["command prefix"]
    bot = commands.Bot(command_prefix=PREFIX, intents=intents)
    TOKEN = settings_file["token"]


# load commands
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")


@bot.event
async def on_ready():
    print("bot is up and ready.")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"'{PREFIX}' prefix"))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('***:x: Ops you __can not__ use this command***')

    if isinstance(error, commands.CommandNotFound):
        pass


bot.run(TOKEN)
