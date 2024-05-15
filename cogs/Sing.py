import discord  
from discord.ext import commands
import logging
from typing import cast
import wavelink



class Sing(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = {} 
        self.isSinging = {}

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("Sing.py is ready!")


    @commands.command(name="join")
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel!")

        await ctx.author.voice.channel.connect()
        await ctx.send("Joined your voice channel!")

    @commands.command(name="play", aliases=["p"])
    async def play(self,ctx: commands.Context, *, query: str) -> None:
        try:
            """Play a song with the given query."""
            if not ctx.guild:
                return

            player: wavelink.Player
            player = cast(wavelink.Player, ctx.voice_client)  # type: ignore

            if not player:
                try:
                    player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
                except AttributeError:
                    await ctx.send("Please join a voice channel first before using this command.")
                    return
                except discord.ClientException:
                    await ctx.send("I was unable to join this voice channel. Please try again.")
                    return

            # Turn on AutoPlay to enabled mode.
            # enabled = AutoPlay will play songs for us and fetch recommendations...
            # partial = AutoPlay will play songs for us, but WILL NOT fetch recommendations...
            # disabled = AutoPlay will do nothing...
            player.autoplay = wavelink.AutoPlayMode.enabled

            # Lock the player to this channel...
            if not hasattr(player, "home"):
                player.home = ctx.channel
            elif player.home != ctx.channel:
                await ctx.send(f"You can only play songs in {player.home.mention}, as the player has already started there.")
                return

            # This will handle fetching Tracks and Playlists...
            # Seed the doc strings for more information on this method...
            # If spotify is enabled via LavaSrc, this will automatically fetch Spotify tracks if you pass a URL...
            # Defaults to YouTube for non URL based queries...
            tracks: wavelink.Search = await wavelink.Playable.search(query)
            if not tracks:
                await ctx.send(f"{ctx.author.mention} - Could not find any tracks with that query. Please try again.")
                return

            if isinstance(tracks, wavelink.Playlist):
                # tracks is a playlist...
                added: int = await player.queue.put_wait(tracks)
                await ctx.send(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
            else:
                track: wavelink.Playable = tracks[0]
                await player.queue.put_wait(track)
                await ctx.send(f"Added **`{track}`** to the queue.")

            if not player.playing:
                # Play now since we aren't playing anything...
                await player.play(player.queue.get(), volume=30)

            # Optionally delete the invokers message...
            try:
                await ctx.message.delete()
            except discord.HTTPException:
                pass
        except Exception as e:
            logging.error(e)
    
    @commands.command(name="skip", aliases=["sk","s"])
    async def skip(self,ctx: commands.Context) -> None:
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.skip(force=True)
        await ctx.message.add_reaction("\u2705")


    @commands.command(name="toggle", aliases=["pause", "resume"])
    async def pause_resume(self,ctx: commands.Context) -> None:
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.pause(not player.paused)
        await ctx.message.add_reaction("\u2705")


    @commands.command(name="vol", aliases=["volume"])
    async def volume(self,ctx: commands.Context, value: int) -> None:
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.set_volume(value)
        await ctx.message.add_reaction("\u2705")


    @commands.command(aliases=["dc"])
    async def disconnect(self,ctx: commands.Context) -> None:
        """Disconnect the Player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.disconnect()
        await ctx.message.add_reaction("\u2705")

async def setup(client):
    await client.add_cog(Sing(client))