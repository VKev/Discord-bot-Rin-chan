import discord  
from discord.ext import commands
import asyncio
import yt_dlp
import pywhatkit
import requests
from bs4 import BeautifulSoup
import os
os.environ['DISPLAY'] = ':0'


yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.4"'}

def is_url(string):
    if string.startswith(("http://", "https://", "ftp://")):
        return True
    else:
        return False


def get_video_title(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_element = soup.find('title')
        if title_element:
            title = title_element.text
            return title
        else:
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

class Sing(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = {} 
        self.isSinging = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.client.user:  
            if before.channel and not after.channel:  
                server_id = before.channel.guild.id
                if server_id in self.queues:
                    self.queues[server_id].clear()
                    self.isSinging[server_id] = False


    @commands.Cog.listener()
    async def on_ready(seft):
        print("Sing.py is ready!")

    async def disconnect_after_delay(self, ctx, delay):
        await asyncio.sleep(delay)
        server_id = ctx.guild.id
        if ctx.voice_client and not ctx.voice_client.is_playing():
            self.queues[server_id].clear()
            self.isSinging[server_id] = False
            await ctx.voice_client.disconnect()

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx, *, content):
        url = content
        server_id = ctx.guild.id

        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        user_voice_channel = ctx.author.voice.channel
        bot_voice_channel = ctx.voice_client.channel if ctx.voice_client else None

        if bot_voice_channel and user_voice_channel != bot_voice_channel:
            await ctx.send("You and the bot are in different voice channels.")
            return

        if not ctx.voice_client:
            try:
                voice_client = await ctx.author.voice.channel.connect()
            except:
                await ctx.send("Cannot connect to voice channel")
                return
            
        else:
            voice_client = ctx.voice_client

        if not is_url(url):
            search_term = pywhatkit.playonyt(content, open_video=False)
            url = requests.get(search_term).url
        
        if self.queues.get(server_id, False) or self.isSinging.get(server_id, False):
            if server_id in self.queues:
                self.queues[server_id].append(url)
            else:
                self.queues[server_id] = [url]
            await ctx.send("Song added to queue!")

        if not voice_client.is_playing():
            if not self.isSinging.get(server_id, False):
                self.isSinging[server_id] = True
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
            song_length = data['duration']
            self.client.loop.create_task(self.disconnect_after_delay(ctx, song_length + 90))
        except Exception as e:
            print(e)

    async def play_next(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.queues and self.queues[server_id]:
            next_song = self.queues[server_id].pop(0)
            await self.play_song(ctx, next_song)
        else:
            self.isSinging[server_id] = False
    
    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await self.play_next(ctx)
        else:
            await ctx.send("I'm not in a voice channel.")
    
    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await self.play_next(ctx)
        else:
            await ctx.send("I'm not in a voice channel.")

    @commands.command(name="queue")
    async def view_queue(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.queues and self.queues[server_id]:
            queue_list = "\n".join([f"{index + 1}. {get_video_title(song)}" for index, song in enumerate(self.queues[server_id])])
            await ctx.send(f"Queue:\n{queue_list}")
        else:
            await ctx.send("Queue is empty!")



async def setup(client):
    await client.add_cog(Sing(client))