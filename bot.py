import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get
import logging
import asyncio
import json
import os

cwd = os.getcwd()
print(f"Current directory: {cwd}")
initial_extensions = ['cogs.admin',
                      'cogs.help',
                      'cogs.music']


token_file = json.load(open(cwd+'/config/token.json'))
bot = commands.Bot(command_prefix = ".",help_command=None,case_insensitive=True)
bot.config_token = token_file['token']

logging.basicConfig(level=logging.INFO) #FOR DEBUGGING PURPOSES ONLY - COMMENT OUT IF YOU NEED CLEAN OUTPUT

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogging in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    
    await bot.change_presence(activity=discord.Game('Type .help'))
    print(f'Successfully logged in and booted...!')


bot.run(bot.config_token)