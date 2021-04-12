import json
import os
import platform
import asyncio

import discord
from discord import Embed
from discord.ext import commands
import discord.utils

cwd = os.getcwd()




class Info(commands.Cog):
    """
    Information related commands
    """
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        bot.version = "0.6.9"
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info loaded\n")
        
    @commands.command()
    async def stats(self, ctx):
        """
        Displays bot statistics.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        #memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=discord.Colour.red(), timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.bot.version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        #embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developers:', value="<@815833086330667008>")

        embed.set_footer(text=f"{self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url="https://cdn.discordapp.com/avatars/815833086330667008/446c182ff64ab5eac646c2bb534b3e58.png?size=128")

        await ctx.send(embed=embed)

    @commands.command()
    async def whois(self, ctx, *, user: discord.Member = None):    
        if user is None:
            user = ctx.author      
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user)+1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Info(bot))