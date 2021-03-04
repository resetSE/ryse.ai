import discord
from discord import Embed
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        


def setup(bot):
    bot.add_cog(Music(bot))
