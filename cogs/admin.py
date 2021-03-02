import discord
from discord import Embed
from discord.ext import commands

class Greetings(commands.Cog):
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
        await ctx.send(f"Done! {member} has been banned with reason '{reason}'")
        print(f"\n{member} was banned from '{guild}' with reason '{reason}'\n")

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        guild = ctx.guild

        await member.kick(reason=reason)
        await ctx.send(f"Done! {member} has been kicked with reason '{reason}'")
        print(f"\n{member} was kicked from '{guild}' with reason '{reason}'\n")

    @commands.command(aliases=['unb'])
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        guild = ctx.guild

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Done! Unbanned {user.name}#{user.discriminator}")
                print(f"'{user.name}#{user.discriminator}' was unbanned from '{guild}'.")

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
    bot.add_cog(Greetings(bot))
