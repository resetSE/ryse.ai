import asyncio
import json
import logging
import os

import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get
from pretty_help import PrettyHelp

cwd = os.getcwd()
print(f"Current directory: {cwd}")

#etc_file = json.load(open(cwd+'/config/etc.json'))
token_file = json.load(open(cwd+'/config/token.json'))

def get_prefix(client, message):
    with open(cwd+'/config/prefixes.json') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = get_prefix, case_insensitive=True, intents = intents, help_command=PrettyHelp())
bot.config_token = token_file['token']


logging.basicConfig(level=logging.INFO) #FOR DEBUGGING PURPOSES ONLY - COMMENT OUT IF YOU NEED CLEAN OUTPUT

@bot.event
async def on_ready():
    print(f'\n\nLogging in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    
    if __name__ == "__main__":
        for file in os.listdir(cwd+"/cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                bot.load_extension(f"cogs.{file[:-3]}")

    await bot.change_presence(activity=discord.Game(f'Try the help command, the default prefix is .'))
    print(f'Login successful! {bot.user.name} is up and running!')

@bot.event
async def on_guild_join(guild):
    with open(cwd+"/config/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."
    with open(cwd+"/config/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open(cwd+"/config/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))
    with open(cwd+"/config/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("No permission!")


bot.run(bot.config_token, reconnect=True)
