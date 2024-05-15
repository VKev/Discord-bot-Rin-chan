import discord 
from discord.ext  import commands, tasks
from discord import app_commands
from itertools import cycle
import os
import asyncio
import pathlib
import wavelink
import logging

import subprocess
import time




lavalink_process = subprocess.Popen(['java', '-jar', 'Lavalink.jar'])
time.sleep(5)

path = pathlib.Path(__file__).parent.resolve()
class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.WaveLink = None
        self.statuses = cycle(["!help", "😀", "😖","😈"])
        super().__init__(*args, **kwargs)
        discord.utils.setup_logging(level=logging.INFO)
        self.initial_extensions = [f"cogs.{file[:-3]}" for file in os.listdir(os.path.join(path, 'cogs')) if file.endswith(".py")]

    async def setup_hook(self):
        nodes = [wavelink.Node(uri="http://127.0.0.1:2333", password="youshallnotpass")]
        self.WaveLink = await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100)

        for ext in self.initial_extensions:
            await self.load_extension(ext)
    
    async def on_ready(self) -> None:
        logging.info("Logged in: %s | %s", client.user, client.user.id)
        try:
            synced = await client.tree.sync()
            logging.info(f"Successfully synced {len(synced)} commands.")
        except Exception as e:
            print(e)
        self.cycle_status.start()
    
    @tasks.loop(minutes=5) 
    async def cycle_status(self):
        status = next(self.statuses)
        await self.change_presence(activity=discord.Game(name=status))

    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        logging.info("Wavelink Node connected: %r | Resumed: %s", payload.node, payload.resumed)

    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        embed: discord.Embed = discord.Embed(title="Now Playing")
        embed.description = f"**{track.title}** by `{track.author}`"

        if track.artwork:
            embed.set_image(url=track.artwork)

        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"

        if track.album.name:
            embed.add_field(name="Album", value=track.album.name)

        await player.home.send(embed=embed)
            

client = MyBot(command_prefix="!", intents=discord.Intents.all(), help_command=None)


@client.event
async def on_command_error(ctx,error):
    if(isinstance(error,commands.MissingRequiredArgument)):
        await ctx.send("Missing required argument")
    if(isinstance(error,commands.MissingPermissions)):
        await ctx.send("You don't have permission! baka!")


@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}", ephemeral=True)

@client.tree.command(name="say")
@app_commands.describe(thing_to_say= "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: {thing_to_say}", ephemeral=True)


async def main():
    async with client:
        await client.start(os.environ.get('DISCORD_BOT_KEY'))

asyncio.run(main())