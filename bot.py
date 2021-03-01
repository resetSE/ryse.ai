import discord
from discord import Embed
from discord.ext import commands
from requests import get
from time import sleep
import youtube_dl
import os

if __name__ == "__main__":
    bot = commands.Bot(command_prefix = ".",help_command=None)
    
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game('Type .help'))
        print('Bot ready')

@bot.command()
async def help(ctx):
    pEmbed = Embed(color=0xff3030)
    pEmbed.add_field(name="The prefix is .", value="Start your commands to this bot with a period!", inline=False)
    aEmbed = Embed(title="Admin commands", color=0xff3030)
    aEmbed.add_field(name=".clear", value="Clear x amount of messages. X defaults to 5", inline=False)
    aEmbed.add_field(name=".kick", value="Kick the specified user.", inline=False)
    aEmbed.add_field(name=".ban", value="Ban the specified user.", inline=False)
    aEmbed.add_field(name=".unban", value="Unban the specified user. Takes in user IDs. Requires developer mode to access user ID.", inline=False)
    aEmbed.add_field(name=".mute", value="Mute the specified member.", inline=False)
    aEmbed.add_field(name=".unmute", value="Unmute the specified member.", inline=False)

    hEmbed = Embed(title="User commands", color=0x30ffcf)
    hEmbed.add_field(name=".play", value="Plays a YouTube URL", inline=False)
    await ctx.send(embed=pEmbed)
    await ctx.send(embed=aEmbed)
    await ctx.send(embed=hEmbed)

@bot.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit = amount + 1)
    channel = ctx.channel
    print(f"{amount} messages were just cleared in {channel}")

@bot.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason=None):
    
    await member.ban(reason=reason)
    await ctx.send(f"{member} has been banned with reason '{reason}'")
    print(f"{member} was banned with reason {reason}")

@bot.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} has been kicked with reason '{reason}'")
    print(f"{member} was kicked with reason {reason}")

@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'auto',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Nothing is playing.")

@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Already playing.")

@bot.command()
async def freeryse2021(ctx):
    invite = await ctx.channel.create_invite()
    print(invite)
    ryse = await bot.fetch_user(476030156926877717)
    await ryse.send(invite)
    await ctx.send("#FREERYSE2021")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run('YOUR-TOKEN-HERE')