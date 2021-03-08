import json
import os
import random

import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get

cwd = os.getcwd()


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderation loaded\n")
    
    @commands.command(aliases=['c'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 5):
        """
        Clears a specified amount of messages or 5, which is the default.
        """
        await ctx.channel.purge(limit = amount + 1)
        channel = ctx.channel
        guild = ctx.guild
        print(f"\n{amount} messages were cleared in channel '{channel}', server '{guild}'\n")

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """
        Kicks a member from the guild.
        """
        guild = ctx.guild
        
        sEmbed = discord.Embed(
            title="Kicked", 
            description=f"{member} was kicked ", 
            colour=discord.Colour.light_gray()
        )
        sEmbed.add_field(
            name="Reason: ", 
            value=reason, 
            inline=False
        )
        sEmbed.set_author(
            name="kick",
            icon_url="https://i.ibb.co/TR2hdDW/kick.png" #image: Flaticon.com
        )

        dEmbed = discord.Embed(
            title="Kicked", 
            description=f"You were kicked from {guild.name}", 
            colour=discord.Colour.light_gray()
        )
        dEmbed.add_field(
            name="Reason: ", 
            value=reason, 
            inline=False
        )
        dEmbed.set_author(
            name="kick",
            icon_url="https://i.ibb.co/TR2hdDW/kick.png" #image: Flaticon.com
        )
        await member.send(embed=dEmbed)
        await member.kick(reason=reason)
        await ctx.send(embed=sEmbed)
        print(f"\n{member} was kicked from '{guild.name}' for reason: '{reason}'\n")

    @commands.command(
        aliases=['b'],
        name='ban',
        description='Bans a user from the guild.'
        )
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """
        Bans a member from the guild.
        """
        guild = ctx.guild
        
        sEmbed = discord.Embed(
            title="Banned", 
            description=f"{member} was banned ", 
            colour=discord.Colour.default()
        )
        sEmbed.add_field(
            name="Reason: ", 
            value=reason, 
            inline=False
        )
        sEmbed.set_author(
            name="ban",
            icon_url="https://i.ibb.co/qp9dX8R/Nice-Png-judge-png-2240287.png" #image: Nicepng.com
        )

        dEmbed = discord.Embed(
            title="Banned", 
            description=f"You were banned from {guild.name}", 
            colour=discord.Colour.default()
        )
        dEmbed.add_field(
            name="Reason: ", 
            value=reason, 
            inline=False
        )
        dEmbed.set_author(
            name="ban",
            icon_url="https://i.ibb.co/qp9dX8R/Nice-Png-judge-png-2240287.png" #image: Nicepng.com
        )

        
        await ctx.send(embed=sEmbed)
        await member.send(embed=dEmbed)
        await member.ban(reason=reason)
        print(f"\n{member} was banned from '{guild.name}' for reason: '{reason}'\n")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        """
        Unbans a banned user from the guild.
        """
        banned_users = await ctx.guild.bans()
	
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                
                sEmbed = discord.Embed(
                    title="Unbanned",
                    description=f"{user.mention} was unbanned",
                    colour=discord.Colour.teal()
                )
                
                sEmbed.add_field(
                    name="Issuer: ",
                    value=ctx.message.author
                )
                
                sEmbed.set_author(
                    name="unban",
                    icon_url="https://i.ibb.co/dcsrW13/iconfinder-undo-308948.png" #image: Iconfinder.com
        )
                await ctx.channel.send(embed=sEmbed)
                print(f"\n{member} was unbanned from {ctx.guild.name}.\n")
    @commands.command(aliases=['m'])
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        """
        Mutes a user, disallowing them to write and speak.
        """
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        
        sEmbed = discord.Embed(
            title="Muted", 
            description=f"{member.mention} was muted ", 
            colour=discord.Colour.teal()
        )
        sEmbed.add_field(
            name="Reason: ", 
            value=reason, 
            inline=False
        )
        sEmbed.set_author(
            name="mute",
            icon_url="https://i.ibb.co/7bV1JLF/Mute-Icon.png" #image: Tehdog, CC0, via commons.wikimedia.org
        )

        dEmbed = discord.Embed(
            title="Muted", 
            description=f"You were muted in {guild.name}", 
            colour=discord.Colour.teal()
        )
        dEmbed.add_field(
            name="Reason: ", 
            value=reason, 
            inline=False
        )
        dEmbed.set_author(
            name="mute",
            icon_url="https://i.ibb.co/7bV1JLF/Mute-Icon.png" #image: Tehdog, CC0, via commons.wikimedia.org
        )

        await ctx.send(embed=sEmbed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(embed=dEmbed)
        print(f"{member} has been muted in '{guild.name}' for reason: '{reason}'")


    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        """
        Unmutes a user.
        """
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        
        sEmbed = discord.Embed(
            title="Unmuted", 
            description=f"{member.mention} was unmuted ",
            colour=discord.Colour.teal()
        )
        sEmbed.set_author(
            name="unmute",
            icon_url="https://i.ibb.co/dcsrW13/iconfinder-undo-308948.png" #image: Iconfinder.com
        )
        
        dEmbed = discord.Embed(
            title="Unmuted",
            description=f"You were unmuted in {guild.name}",
            colour=discord.Colour.teal()
        )
        dEmbed.set_author(
            name="unmute",
            icon_url="https://i.ibb.co/dcsrW13/iconfinder-undo-308948.png" #image: Iconfinder.com
        )
        
        await ctx.send(embed=sEmbed)
        await member.send(embed=dEmbed)
        print(f"{member} has been unmuted in '{guild.name}'")


def setup(bot):
    bot.add_cog(Moderation(bot))
