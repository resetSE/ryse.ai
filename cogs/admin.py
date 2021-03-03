import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get



class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=['c'])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount = 5):
            await ctx.channel.purge(limit = amount + 1)
            channel = ctx.channel
            guild = ctx.guild
            print(f"\n{amount} messages were cleared in channel '{channel}', server '{guild}'\n")
    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        guild = ctx.guild

        await member.ban(reason=reason)
        await ctx.send(f"{member} has been banned for reason: '{reason}'")
        print(f"\n{member} was banned from '{guild.name}' for reason: '{reason}'\n")

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        guild = ctx.guild

        await member.kick(reason=reason)
        await ctx.send(f"{member} has been kicked for reason: '{reason}'")
        print(f"\n{member} was kicked from '{guild.name}' for reason: '{reason}'\n")

    @commands.command(aliases=['unb'])
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member : discord.Member, *, reason=None):
        guild = ctx.guild

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.name}#{user.discriminator}")
                print(f"'{user.name}#{user.discriminator}' was unbanned from '{guild}'.")

    @commands.command(aliases=['m'])
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        
        sEmbed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
        sEmbed.add_field(name="Reason: ", value=reason, inline=False)

        dEmbed = discord.Embed(title="Muted", description=f"You were muted in {guild.name}", colour=discord.Colour.light_gray())
        dEmbed.add_field(name="Reason: ", value=reason, inline=False)

        await ctx.send(embed=sEmbed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(embed=dEmbed)
        print(f"{member} has been muted in '{guild.name}' for reason: '{reason}'")


    @commands.command(description="Unmutes a specified user.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        sEmbed = discord.Embed(title="Unmuted", description=f"{member.mention} was unmuted ",colour=discord.Colour.light_gray())
        dEmbed = discord.Embed(title="Unmuted", description=f"You were unmuted in {guild.name}",colour=discord.Colour.light_gray())
        await ctx.send(embed=sEmbed)
        await member.send(embed=dEmbed)
        print(f"{member} has been unmuted in '{guild.name}'")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def load(self, ctx, name: str):
        self.bot.load_extension(f"cogs.{name}")
        await ctx.send(f"Loaded extension **{name}.py**")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unload(self, ctx, name: str):
        self.bot.unload_extension(f"cogs.{name}")
        await ctx.send(f"Unloaded extension **{name}.py**")

def setup(bot):
    bot.add_cog(Admin(bot))
