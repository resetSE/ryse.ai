import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get
import asyncio
import youtube_dl
import os

initial_extensions = ['cogs.admin']

bot = commands.Bot(command_prefix = ".",help_command=None)

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogging in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    
    await bot.change_presence(activity=discord.Game('Type .help'))
    print(f'Successfully logged in and booted...!')


bot.run('YOUR-TOKEN-HERE')