import json
import os
import platform
import asyncio

import discord
from discord import Embed
from discord.ext import commands

cwd = os.getcwd()


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        bot.version = "0.6.9"
    @commands.Cog.listener()
    async def on_ready(self):
        print("admin loaded\n")
        
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
            
    @commands.command(aliases=['pref', 'pr'])
    @commands.has_permissions(administrator = True)
    async def prefix(self, ctx, prefix):
        """
        Changes the bot's prefix on a per-server basis
        """
        with open(cwd+'/config/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open(cwd+'/config/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        
        sEmbed = discord.Embed(
            title="Prefix changed",
            description=f"{prefix} is the new prefix",
            colour=discord.Colour.green()
        )
        sEmbed.set_author(
            name="Success",
            icon_url="https://i.ibb.co/JCJzkh2/iconfinder-checkmark-24-103184.png" #image: Iconfinder.com
        )
        
        await ctx.send(embed=sEmbed)
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def load(self, ctx, name: str):
        """
        Loads a cog.
        """
        sEmbed = discord.Embed(
            title="Loaded",
            description=f"**{name}** was loaded",
            colour=discord.Colour.green()
        )
        sEmbed.set_author(
            name="Success",
            icon_url="https://i.ibb.co/JCJzkh2/iconfinder-checkmark-24-103184.png" #image: Iconfinder.com
        )
        self.bot.load_extension(f"cogs.{name}")
        await ctx.send(embed=sEmbed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unload(self, ctx, name: str):
        """
        Unloads a cog.
        """
        eEmbed = discord.Embed(
            title="Can't unload",
            description=f"**{name}** contains important functionality!",
            colour=discord.Colour.red()
        )
        eEmbed.set_author(
            name="Error",
            icon_url="https://i.ibb.co/Sw0pYmS/cross-icon-29.png" #image: Icon-library.com
        )
        
        sEmbed = discord.Embed(
            title="Unloaded",
            description=f"**{name}** was unloaded",
            colour=discord.Colour.green()
        )
        sEmbed.set_author(
            name="Success",
            icon_url="https://i.ibb.co/JCJzkh2/iconfinder-checkmark-24-103184.png" #image: Iconfinder.com
        )
        
        if(name in ['admin']):
            await ctx.send(embed=eEmbed)
            return
        self.bot.unload_extension(f"cogs.{name}")
        await ctx.send(embed=sEmbed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def reload(self, ctx, name: str):
        """
        Reloads a cog.
        """
        sEmbed = discord.Embed(
            title="Reloaded",
            description=f"**{name}** was reloaded",
            colour=discord.Colour.green()
        )
        sEmbed.set_author(
            name="Success",
            icon_url="https://i.ibb.co/JCJzkh2/iconfinder-checkmark-24-103184.png" #image: Iconfinder.com
        )
        self.bot.unload_extension(f"cogs.{name}")
        await asyncio.sleep(1)
        self.bot.load_extension(f"cogs.{name}")
        await ctx.send(embed=sEmbed)
def setup(bot):
    bot.add_cog(Admin(bot))
