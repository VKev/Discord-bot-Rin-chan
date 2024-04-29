import discord  
from discord.ext import commands
import asyncio
import yt_dlp
import pywhatkit
import requests

yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.4"'}

queue = []
def is_url(string):
    if string.startswith(("http://", "https://", "ftp://")):
        return True
    else:
        return False

class Sing(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(seft):
        print("Sing.py is ready!")

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *, content):
        global queue  # Access the global queue variable

        url = content
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        user_voice_channel = ctx.author.voice.channel
        bot_voice_channel = ctx.voice_client.channel if ctx.voice_client else None

        if bot_voice_channel and user_voice_channel != bot_voice_channel:
            await ctx.send("You and the bot are in different voice channels.")
            return

        if not ctx.voice_client:
            voice_client = await ctx.author.voice.channel.connect()
        else:
            voice_client = ctx.voice_client

        if not is_url(url):
            search_term = pywhatkit.playonyt(content, open_video=False)
            url = requests.get(search_term).url;

        if voice_client.is_playing() or queue:
            queue.append(url)
            await ctx.send("Song added to queue!")
        else:
            await self.play_song(ctx, url)

    async def play_song(self, ctx, url):
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
            voice_client = ctx.voice_client
            await ctx.send(f"Now playing {url}")
            voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.client.loop))
        except Exception as e:
            print(e)

    async def play_next(self, ctx):
        global queue
        if queue:
            next_song = queue.pop(0)
            await self.play_song(ctx, next_song)
    
    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await self.play_next(ctx)
        else:
            await ctx.send("I'm not in a voice channel.")

    @commands.command(name="queue")
    async def view_queue(self, ctx):
        if queue:
            queue_list = "\n".join([f"{index + 1}. {song}" for index, song in enumerate(queue)])
            await ctx.send(f"Queue:\n{queue_list}")
        else:
            await ctx.send("Queue is empty!")



async def setup(client):
    await client.add_cog(Sing(client))