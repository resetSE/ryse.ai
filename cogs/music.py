import discord
import wavelink
from discord import Embed, utils
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=2333,
                                              rest_uri='http://127.0.0.1:2333',
                                              password='youshallnotpass',
                                              identifier='TEST',
                                              region='eu')

    @commands.command(name='connect')
    async def _connect(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

    @commands.command()
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')
        
        sEmbed = discord.Embed(
            title="Added to queue", 
            description=f'Added {str(tracks[0])} to the queue.',
            colour=discord.Colour.teal()
        )
        sEmbed.set_author(
            name="play",
            icon_url="https://i.ibb.co/VgsfXHB/iconfinder-music-172510.png" #image: Iconfinder.com
        )

        eEmbed = discord.Embed(
            title="Error", 
            description="Couldn't find any songs with that query",
            colour=discord.Colour.red()
        )
        eEmbed.set_author(
            name="play",
            icon_url="https://i.ibb.co/Sw0pYmS/cross-icon-29.png" #image: Icon-library.com
        )

        if not tracks:
            await ctx.send(embed=eEmbed)
#
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await player.stop()
            await ctx.invoke(self._connect)

        await ctx.send(embed=sEmbed)
        await player.set_volume(35)
        await player.play(tracks[0])


    @commands.command()
    async def play(self, ctx, *, query: str):
        eEmbed = discord.Embed(
            title="Error", 
            description="Couldn't find any songs with that query",
            colour=discord.Colour.red()
        )
        eEmbed.set_author(
            name="play",
            icon_url="https://i.ibb.co/Sw0pYmS/cross-icon-29.png" #image: Icon-library.com
        )

        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send(embed=eEmbed)

        sEmbed = discord.Embed(
            title="Added to queue", 
            description=f'Added {str(tracks[0])} to the queue.',
            colour=discord.Colour.teal()
        )
        sEmbed.set_author(
            name="play",
            icon_url="https://i.ibb.co/VgsfXHB/iconfinder-music-172510.png" #image: Iconfinder.com
        )

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self._connect)

        await ctx.send(embed=sEmbed)
        await player.play(tracks[0])


    @commands.command()
    async def stop(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        sEmbed = discord.Embed(
            title="Stopped", 
            description="Stopped playing music",
            colour=discord.Colour.teal()
        )
        sEmbed.set_author(
            name="stop",
            icon_url="https://i.ibb.co/VgsfXHB/iconfinder-music-172510.png" #image: Iconfinder.com
        )


        eEmbed = discord.Embed(
            title="Error", 
            description="Not playing anything",
            colour=discord.Colour.red()
        )
        eEmbed.set_author(
            name="stop",
            icon_url="https://i.ibb.co/Sw0pYmS/cross-icon-29.png" #image: Icon-library.com
        )

        if player.is_playing:
            await player.stop()
            await player.disconnect()
            await ctx.send(embed=sEmbed)
        else:
            await ctx.send(embed=eEmbed)

    @commands.command()
    async def disconnect(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)

        sEmbed = discord.Embed(
            title="Error", 
            description="Not in a channel",
            colour=discord.Colour.teal()
        )
        sEmbed.set_author(
            name="stop",
            icon_url="https://i.ibb.co/VgsfXHB/iconfinder-music-172510.png" #image: Iconfinder.com
        )


        if player.is_connected:
            await player.stop()
            await player.disconnect()
        
        else: 
            await ctx.send(embed=sEmbed)
def setup(bot):
    bot.add_cog(Music(bot))
