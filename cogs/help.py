import discord
from discord import Embed
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def help(self, ctx):
        pEmbed = Embed(color=0x3030ff)
        pEmbed.add_field(name="The prefix is .", value="Start your commands to this bot with a period!", inline=False)
        aEmbed = Embed(title="Admin commands", color=0xff3030)
        aEmbed.add_field(name=".clear", value="Clear x amount of messages. X defaults to 5", inline=False)
        aEmbed.add_field(name=".kick", value="Kick the specified user.", inline=False)
        aEmbed.add_field(name=".ban", value="Ban the specified user.", inline=False)
        aEmbed.add_field(name=".unban", value="Unban the specified user. Takes in user IDs. Requires developer mode to access user ID.", inline=False)
        aEmbed.add_field(name=".mute", value="Mute the specified member.", inline=False)
        aEmbed.add_field(name=".unmute", value="Unmute the specified member.", inline=False)

        #hEmbed = Embed(title="User commands", color=0x30ffcf)
        #hEmbed.add_field(name=".play", value="Plays a YouTube URL", inline=False)
        await ctx.send(embed=pEmbed)
        await ctx.send(embed=aEmbed)
        #await ctx.send(embed=hEmbed)

def setup(bot):
    bot.add_cog(Help(bot))
