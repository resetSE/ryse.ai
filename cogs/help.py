import re
import math
import random
import os
import json

import discord
from discord import Embed
from discord.ext import commands

cwd = os.getcwd()

def get_prefix(client, message):
    with open(cwd+'/config/prefixes.json') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

prefix = get_prefix

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=['h'])
    async def help2(self, ctx):
        hEmbed = discord.Embed(
            title="Help",
            color=discord.Colour.teal()
        )
        hEmbed.set_author(
            name=f".help",
            icon_url="https://i.ibb.co/Cb87H4w/iconfinder-question-1608802.png" #image: Iconfinder.com
        )

        await ctx.send(embed=hEmbed)
def setup(bot):
    bot.add_cog(Help(bot))
